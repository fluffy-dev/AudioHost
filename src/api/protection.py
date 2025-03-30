from typing import Optional, Annotated
from fastapi import Depends

from fastapi import HTTPException, Cookie

from src.api.auth.dtos.token import AccessTokenDTO
from src.apps.auth.depends.service import IAuthService
from src.apps.user.dto import UserDTO


async def authenticated_user(auth_service: IAuthService, access_token: Optional[str] = Cookie(default=None)) -> Optional[UserDTO]:
    if access_token is None:
        raise HTTPException(status_code=403, detail="Access token missing")

    try:
        return await auth_service.get_current_user(AccessTokenDTO(access_token=access_token))
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

AuthUser = Annotated[UserDTO, Depends(authenticated_user)]

async def admin_user(auth_user: AuthUser):

    if not auth_user.is_admin:
        raise HTTPException(status_code=403, detail="You are not an admin")

    return auth_user

AdminUser = Annotated[UserDTO, Depends(admin_user)]