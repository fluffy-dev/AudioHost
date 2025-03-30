from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    yandex_client_id: str = Field(..., alias="YANDEX_CLIENT_ID")
    yandex_client_secret: str = Field(..., alias="YANDEX_CLIENT_SECRET")
    yandex_redirect_uri: str = Field("http://localhost:8000/auth/yandex/callback", alias="YANDEX_REDIRECT_URI")
    internal_secret: str = Field(..., alias="INTERNAL_SECRET")
    internal_token_expire_hours: int = Field(1, alias="INTERNAL_TOKEN_EXPIRE_HOURS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
