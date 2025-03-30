from fastapi import Depends
from typing import Annotated

from src.apps.audio.repositories.audio_file import AudioFileRepository

IAudioFileRepository = Annotated[AudioFileRepository, Depends()]