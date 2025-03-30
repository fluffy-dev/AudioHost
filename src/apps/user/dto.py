from pydantic import BaseModel, EmailStr, constr


class FindUserDTO(BaseModel):
    id: int = None
    name: constr(max_length=20) = None
    surname: constr(max_length=20) = None
    email: EmailStr = None


class UserDTO(BaseModel):
    id: int = None
    name: constr(max_length=20)
    surname: constr(max_length=20)
    email: EmailStr
    password: str = None
    is_admin: bool = False


class UpdateUserDTO(BaseModel):
    pass


class UserBaseDTO(BaseModel):
    id: int = None
    name: str = None
    surname: str = None
    email: EmailStr = None
    password: str = None

