from pydantic_settings import BaseSettings
from pydantic import Field

class ConfigToken(BaseSettings):
    ACCESS_TOKEN_LIFETIME: int = Field(300, alias="ACCESS_TOKEN_LIFETIME")
    REFRESH_TOKEN_LIFETIME: int = Field(86400, alias="REFRESH_TOKEN_LIFETIME")
    REFRESH_TOKEN_ROTATE_MIN_LIFETIME: int = Field(3600, alias="REFRESH_TOKEN_ROTATE_MIN_LIFETIME")


config_token = ConfigToken()
