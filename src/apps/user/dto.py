from typing import Optional
from src.libs.base_dto import BaseDto

class UserDTO(BaseDto):
    id: int
    name: str
    surname: Optional[str] = None
    email: str
    password: str
    is_admin: bool

class UpdateUserDTO(BaseDto):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

class FindUserDTO(BaseDto):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
