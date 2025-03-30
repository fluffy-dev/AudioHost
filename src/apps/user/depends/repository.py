from fastapi import Depends
from typing import Annotated

from src.apps.user.repositories.user import UserRepository

IUserRepository = Annotated[UserRepository, Depends()]