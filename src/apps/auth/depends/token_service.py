from fastapi import Depends
from typing import Annotated

from src.apps.auth.token_service import TokenService

ITokenService = Annotated[TokenService, Depends()]