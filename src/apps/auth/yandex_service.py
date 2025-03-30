import httpx

from src.api.yandex.dtos.yandex import CallBackCodeDTO

from src.apps.auth.depends.token_service import ITokenService
from src.apps.user.depends.service import IUserService
from src.apps.user.dto import UserDTO, FindUserDTO
from src.apps.user.entity import UserEntity
from src.libs.exceptions import AlreadyExistError

class YandexService:
    def __init__(self, token_service: ITokenService, user_service: IUserService):
        self.token_service = token_service
        self.user_service = user_service

        self.client_id = ""
        self.client_secret = ""
        self.redirect_uri = ""
        self.internal_token_expire_hours = 10 #hours

        self.auth_url = "https://oauth.yandex.com/authorize"
        self.token_url = "https://oauth.yandex.com/token"
        self.user_info_url = "https://login.yandex.ru/info"

    async def redirect_to_login(self):
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri
        }

        url = httpx.URL(self.auth_url).copy_merge_params(params)

        return str(url)

    async def catch_user(self, user_data: dict) -> UserDTO:
        user_entity = UserEntity(name=user_data.get("first_name", "John"),
                            surname=user_data.get("last_name", "Doe"),
                            email=user_data.get("default_email"),
                            password=user_data.get("client_id")
                            )
        try:
            return await self.user_service.create(user_entity)
        except AlreadyExistError as e:
            return await self.user_service.get_user(FindUserDTO(email=user_data.get("default_email")))

    async def get_access_token(self, dto:CallBackCodeDTO):
        token_payload = {
            "grant_type": "authorization_code",
            "code": dto.code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
        }
        async with httpx.AsyncClient() as client:
            token_response = await client.post(self.token_url, data=token_payload)

        if token_response.status_code != 200:
            raise RuntimeError(f"Token exchange failed with status {token_response.status_code}")

        token_json = token_response.json()
        access_token = token_json.get("access_token")

        if access_token is None:
            raise RuntimeError(f"Failed to fetch access token")

        return access_token

    async def catch_user_data(self, access_token:str):
        headers = {"Authorization": f"OAuth {access_token}"}

        async with httpx.AsyncClient() as client:
            user_response = await client.get(self.user_info_url, headers=headers)

        if user_response.status_code != 200:
            raise RuntimeError(f"User info request failed with status {user_response.status_code}")

        return user_response.json()

    async def catch_callback(self, dto: CallBackCodeDTO):
        access_token = await self.get_access_token(dto)

        user_data = await self.catch_user_data(access_token)

        user = await self.catch_user(user_data)

        return await self.token_service.create_tokens(user)



