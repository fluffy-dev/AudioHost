from dataclasses import dataclass


@dataclass
class AudioFileEntity:
    user_id: int
    file_name: str
    file_description: str
    file_path: str
    file_size: int
