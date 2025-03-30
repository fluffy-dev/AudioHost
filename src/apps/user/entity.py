import secrets
import string
from dataclasses import dataclass
from src.config.security import settings
from argon2 import PasswordHasher
from pydantic import EmailStr


@dataclass
class UserEntity:
    name: str
    surname: str
    email: EmailStr
    name_telegram: str
    nick_telegram: str
    nick_google_meet: str
    nick_gitlab: str
    nick_github: str
    role_id: int | None = None
    password: str | None = None
    is_admin: bool | None = None


    def __post_init__(self):
        if self.password is not None:
            self.password = self.hash_password(self.password)

    @staticmethod
    def hash_password(password: str) -> str:
        salt = settings.secret_key
        hashed = PasswordHasher().hash(password.encode("utf-8"), salt=salt.encode("utf-8"))
        return hashed

    @classmethod
    def set_password(cls, password: str) -> str:
        return cls.hash_password(password)
