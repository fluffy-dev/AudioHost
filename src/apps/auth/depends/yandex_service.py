from fastapi import Depends
from typing import Annotated

from src.apps.auth.yandex_service import YandexService

IYandexService = Annotated[YandexService, Depends()]