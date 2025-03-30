from src.libs.base_dto import BaseDto
from datetime import datetime
from typing import Optional

class AudioFileDTO(BaseDto):
    id: int
    file_name: str
    file_path: str
