from src.api.auth.dtos.token import RefreshTokenDTO
from src.libs.exceptions import RegistrationError, AlreadyExistError

from src.api.auth.dtos.registration import RegistrationDTO
from src.api.auth.dtos.login import LoginDTO

from src.apps.user.dto import FindUserDTO, UserDTO, UserBaseDTO
from src.apps.user.entity import UserEntity
from src.apps.user.depends.service import IUserService

from src.apps.auth.depends.token_service import ITokenService


class AuthService:
    def __init__(self, user_service: IUserService, token_service: ITokenService):
        self.user_service = user_service
        self.token_service = token_service

    async def registration(self, dto: RegistrationDTO):
        registration_data = dto.model_dump()
        registration_data.pop("password2", None)
        user_entity = UserEntity(**registration_data)
        try:
            return await self.user_service.create(user_entity)
        except AlreadyExistError as e:
            raise RegistrationError(e)

    async def login(self, dto: LoginDTO):
        user: UserDTO = await self.user_service.get_user(dto=FindUserDTO(email=dto.email))

        dto_hash = UserEntity.hash_password(dto.password)

        if not user or user.password != dto_hash:
            raise ValueError("Invalid password or login")
        return await self.token_service.create_tokens(user)

    async def refresh(self, dto: RefreshTokenDTO):
        payload = await self.token_service.decode_token(dto.refresh_token)

        if payload.get("token_type") != "refresh":
            raise ValueError("Invalid refresh token")

        user_info = payload.get("user")

        return await self.token_service.create_tokens(UserBaseDTO(id=user_info["user_id"], name=user_info["user_name"]))
