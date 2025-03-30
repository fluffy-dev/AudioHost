from typing import Optional, Annotated
from fastapi import Depends

from fastapi import HTTPException, Cookie

from src.apps.auth.depends.service import IAuthService
from src.apps.user.dto import UserDTO


async def authenticated_user(auth_service: IAuthService, access_token: Optional[str] = Cookie(default=None)) -> Optional[UserDTO]:
    if access_token is None:
        raise HTTPException(status_code=403, detail="Access token missing")

    try:
        return await auth_service.get_current_user(access_token)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))


async def admin_user(auth_service: IAuthService, access_token: Optional[str] = Cookie(default=None)):
    if access_token is None:
        raise HTTPException(status_code=401, detail="Access token missing")

    try:
        user = await auth_service.get_current_user(access_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="You are not an admin")

    return user

AdminUser = Annotated[admin_user, Depends()]
AuthUser = Annotated[authenticated_user, Depends()]