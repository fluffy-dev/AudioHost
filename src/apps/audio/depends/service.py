from fastapi import Depends
from typing import Annotated

from src.apps.audio.service import AudioService


IAudioService = Annotated[AudioService, Depends()]