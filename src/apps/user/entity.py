from dataclasses import dataclass
from src.config.security import settings
from argon2 import PasswordHasher
from pydantic import EmailStr


@dataclass
class UserEntity:
    name: str
    surname: str
    email: EmailStr | str
    password: str | None = None

    is_admin: bool  = False

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
