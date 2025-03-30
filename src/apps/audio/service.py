import os
import uuid
import aiofiles
import os.path
from fastapi import HTTPException, UploadFile
from typing import List
from src.apps.audio.models.audio_file import AudioFileModel
from src.apps.audio.depends.repository import IAudioFileRepository
from src.apps.audio.dto import AudioFileDTO


class AudioService:
    def __init__(self, repository: IAudioFileRepository):
        self.repository = repository

        self.storage_dir = os.environ.get("AUDIO_STORAGE_PATH", "uploads/audio")

        os.makedirs(self.storage_dir, exist_ok=True)

    async def upload_file(self, file: UploadFile, user_id: int) -> AudioFileDTO:
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(self.storage_dir, unique_filename)


        try:
            async with aiofiles.open(file_path, "wb") as out_file:
                content = await file.read()
                await out_file.write(content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

        # Create an audio file model instance and persist it using the repository
        audio_file_model = AudioFileModel(
            user_id=user_id,
            file_name=file.filename,
            file_path=file_path,
        )
        created_file = await self.repository.create_audio_file(audio_file_model)

        return AudioFileDTO(
            id=created_file.id,
            file_name=created_file.file_name,
            file_path=created_file.file_path,
            uploaded_at=created_file.uploaded_at,
        )

    async def list_audio_files(self, user_id: int) -> List[AudioFileDTO]:
        files = await self.repository.get_audio_files_by_user(user_id)
        return [
            AudioFileDTO(
                id=file.id,
                file_name=file.file_name,
                file_path=file.file_path,
                uploaded_at=file.uploaded_at,
            )
            for file in files
        ]
