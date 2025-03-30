from src.libs.base_dto import BaseDto


class AudioFileDTO(BaseDto):
    id: int
    file_name: str
    file_description: str
    file_path: str
    file_size: int

class UploadFileDTO(BaseDto):
    file_description: str
    user_id: int