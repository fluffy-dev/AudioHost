from fastapi import Depends
from typing import Annotated

from src.apps.user.service import UserService

IUserService = Annotated[UserService, Depends()]
