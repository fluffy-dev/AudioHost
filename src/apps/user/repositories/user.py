from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from src.libs.exceptions import AlreadyExistError
from src.apps.user.entity import UserEntity
from src.config.database.session import ISession
from src.apps.user.models.user import UserModel
from src.apps.user.dto import UpdateUserDTO, UserDTO, FindUserDTO


class UserRepository:
    model = UserModel

    def __init__(self, session: ISession):
        self.session = session

    async def create(self, user: UserEntity) -> UserDTO:
        instance = UserModel(**user.__dict__)
        self.session.add(instance)
        try:
            await self.session.commit()
        except IntegrityError:
            raise AlreadyExistError(f'{instance.email} is already exist')
        await self.session.refresh(instance)
        return self._get_dto(instance)

    async def get_user(self, dto: FindUserDTO) -> UserDTO | None:
        stmt = select(self.model).filter_by(**dto.model_dump(exclude_none=True))
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        return self._get_dto(result) if result else None

    async def get_list(self, limit: int) -> list[UserDTO]:
        stmt = select(self.model).limit(limit)
        results = (await self.session.execute(stmt)).scalars().all()
        return [self._get_dto(row) for row in results]

    async def get(self, pk: int) -> UserDTO | None:
        stmt = select(self.model).filter_by(id=pk)
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        return self._get_dto(result) if result else None

    async def update(self, dto: UpdateUserDTO, pk: int) -> UserDTO:
        stmt = (
            update(self.model)
            .values(**dto.model_dump(exclude_none=True))
            .filter_by(id=pk)
            .returning(self.model)
        )
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        await self.session.commit()
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return self._get_dto(result)

    async def delete(self, pk: int) -> None:
        stmt = delete(self.model).where(self.model.id == pk)
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_password(self, new_password: str, pk: int) -> UserDTO:
        stmt = (
            update(self.model)
            .values(password=new_password)
            .filter_by(id=pk)
            .returning(self.model)
        )
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        await self.session.commit()
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return self._get_dto(result)

    def _get_dto(self, row: UserModel) -> UserDTO:
        return UserDTO(
            id=row.id,
            name=row.name,
            surname=row.surname,
            email=row.email,
        )
