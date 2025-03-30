from pydantic import BaseModel


class TokenDTO(BaseModel):
    access_token: str
    refresh_token: str

class RefreshTokenDTO(BaseModel):
    refresh_token: str

class AccessTokenDTO(BaseModel):
    access_token: str