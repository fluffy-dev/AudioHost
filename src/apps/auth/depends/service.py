from fastapi import Depends
from typing import Annotated

from src.apps.auth.service import AuthService

IAuthService = Annotated[AuthService, Depends()]