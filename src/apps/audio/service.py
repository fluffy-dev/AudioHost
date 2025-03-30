import os
import uuid
import aiofiles
import os.path
from fastapi import  UploadFile
from typing import List
from src.apps.audio.depends.repository import IAudioFileRepository
from src.apps.audio.dto import AudioFileDTO, UploadFileDTO
from src.apps.audio.entity import AudioFileEntity


class AudioService:
    def __init__(self, repository: IAudioFileRepository):
        self.repository = repository

        self.storage_dir = os.path.join(os.getcwd(), os.environ.get("AUDIO_STORAGE_PATH", "uploads/audio"))

        os.makedirs(self.storage_dir, exist_ok=True)

    async def get_data(self, pk: int, user_id: int) -> AudioFileDTO:
        file_data = await self.repository.get(pk)
        if file_data.user_id != user_id:
            raise ValueError("Forbidden")

        return file_data

    async def upload_file(self, file: UploadFile, dto: UploadFileDTO) -> AudioFileDTO:
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(self.storage_dir, unique_filename)

        try:
            async with aiofiles.open(file_path, "wb") as out_file:
                content = await file.read()
                await out_file.write(content)
        except Exception as e:
            raise RuntimeError(f"Failed to upload file {e}")

        entity = AudioFileEntity(file_path=file_path,
                                 file_name=unique_filename,
                                 file_size=os.path.getsize(file_path),
                                 file_description=dto.file_description,
                                 user_id=dto.user_id)

        return await self.repository.create(entity)

    async def list_audio_files(self, user_id: int) -> List[AudioFileDTO]:
        return await self.repository.get_by_user(user_id)
