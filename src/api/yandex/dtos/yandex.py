from pydantic import BaseModel


class CallBackCodeDTO(BaseModel):
    code: str