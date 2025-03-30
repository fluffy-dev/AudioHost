from pydantic import BaseModel


class BaseDto(BaseModel):
    """Basic Pydantic DTO"""
    class Config:
        from_attributes = True
