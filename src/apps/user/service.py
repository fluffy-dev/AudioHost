from src.apps.user.depends.repository import IUserRepository
from src.apps.user.dto import FindUserDTO, UserDTO
from src.apps.user.entity import UserEntity


class UserService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def create(self, entity: UserEntity) -> UserDTO:
        return await self.repository.create(entity)

    async def get_user(self, dto: FindUserDTO) -> UserDTO:
        return await self.repository.get_user(dto)
    