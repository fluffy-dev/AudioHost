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



class UpdateUserDTO(BaseModel):
    pass