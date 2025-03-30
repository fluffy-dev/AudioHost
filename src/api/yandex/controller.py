
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from src.apps.auth.depends.yandex_service import IYandexService


router = APIRouter(prefix="/auth/yandex", tags=["yandex"])


@router.post("/login")
async def login(service: IYandexService):

    try:
        url = await service.redirect_to_login()
        return RedirectResponse(url=url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/callback")
async def callback(request: Request, service: IYandexService):
    code = request.query_params.get("code")

    if code is None:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    try:
        return await service.catch_callback(code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




