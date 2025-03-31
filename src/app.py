from fastapi import FastAPI

from src.api.routes import router
from src.middleware import init_middleware


def get_app() -> FastAPI:
    app = FastAPI()

    init_middleware(app)

    app.include_router(router)
    return app