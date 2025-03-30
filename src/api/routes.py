from fastapi import APIRouter
from src.api.auth.controller import router as auth_router
from src.api.yandex.controller import router as yandex_router
from src.api.user.controller import router as user_router
from src.api.audio.controller import router as audio_router

router = APIRouter(prefix="/v1", tags=["v1"])
router.include_router(auth_router)
router.include_router(yandex_router)
router.include_router(user_router)
router.include_router(audio_router)
