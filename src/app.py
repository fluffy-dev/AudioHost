import logging
from fastapi import FastAPI

from src.api.routes import router

from src.config.logging import settings as logger_settings, logger_config

def get_app() -> FastAPI:
    if logger_settings.logging_on:
        logging.config.dictConfig(logger_config)
    app = FastAPI()
    app.include_router(router)
    return app
