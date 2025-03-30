from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    yandex_client_id: str = Field(..., alias="YANDEX_CLIENT_ID")
    yandex_client_secret: str = Field(..., alias="YANDEX_CLIENT_SECRET")
    yandex_redirect_uri: str = Field("http://localhost:8000/auth/yandex/callback", alias="YANDEX_REDIRECT_URI")



settings = Settings()
