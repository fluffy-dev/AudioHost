from fastapi import APIRouter
from src.api.auth.controller import router as auth_router
from src.api.yandex.controller import router as yandex_router

router = APIRouter(prefix="/v1", tags=["v1"])
router.include_router(auth_router)
router.include_router(yandex_router)
