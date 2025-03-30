from src.apps.user.depends.repository import IUserRepository
from src.apps.user.dto import FindUserDTO, UserDTO, UpdateUserDTO
from src.apps.user.entity import UserEntity


class UserService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def create(self, entity: UserEntity) -> UserDTO:
        return await self.repository.create(entity)

    async def get_user(self, dto: FindUserDTO) -> UserDTO:
        return await self.repository.get_user(dto)

    async def update(self, dto: UpdateUserDTO, pk: int) -> UserDTO:
        return await self.repository.update(dto, pk)

    async def delete(self, pk: int) -> UserDTO:
        return await self.repository.delete(pk)

    async def update_password(self, new_password: str, pk: int) -> UserDTO:
        return await self.repository.update_password(new_password, pk)
    