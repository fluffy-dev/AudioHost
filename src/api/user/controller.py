from typing import Optional

from fastapi import APIRouter, HTTPException

from src.apps.user.depends.service import IUserService

from src.api.protection import AdminUser, AuthUser
from src.apps.user.dto import UserDTO, FindUserDTO, UpdateUserDTO

router = APIRouter(prefix="/user", tags=["user"])



@router.get("/get_user")
async def get_user(dto: FindUserDTO, service: IUserService, admin_user: AdminUser) -> Optional[UserDTO]:
    try:
        return await service.get_user(dto)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/update_user")
async def update_user(dto: UpdateUserDTO, service: IUserService, admin_user: AdminUser) -> Optional[UserDTO]:
    try:
        return await service.update_user(dto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete_user")
async def delete_user(pk: int, service: IUserService, admin_user: AdminUser) -> Optional[UserDTO]:
    try:
        return await service.delete_user(pk)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))




