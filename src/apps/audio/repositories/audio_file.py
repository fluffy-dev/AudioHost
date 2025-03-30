from typing import Optional, List, Type
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError

from src.config.database.session import ISession
from src.apps.audio.models.audio_file import AudioFileModel
from src.apps.audio.dto import AudioFileDTO


class AudioFileRepository:
    model: Type[AudioFileModel] = AudioFileModel

    def __init__(self, session: ISession) -> None:
        self.session: ISession = session

    async def create(self, audio_file: AudioFileModel) -> AudioFileDTO:
        """Creates a new audio file record in the database."""
        self.session.add(audio_file)
        try:
            await self.session.commit()
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"Integrity error: {e}")
        await self.session.refresh(audio_file)
        return self._get_dto(audio_file)

    async def get_by_user(self, user_id: int) -> List[AudioFileDTO]:
        """Retrieves all audio files associated with a given user."""
        stmt = select(self.model).filter_by(user_id=user_id)
        results: List[AudioFileModel] = (await self.session.execute(stmt)).scalars().all()
        return [self._get_dto(row) for row in results]

    async def delete(self, pk: int) -> None:
        """Deletes an audio file record based on its primary key."""
        stmt = delete(self.model).where(self.model.id == pk)
        await self.session.execute(stmt)
        await self.session.commit()

    def _get_dto(self, row: AudioFileModel) -> AudioFileDTO:
        """Converts an AudioFileModel instance to an AudioFileDTO."""
        return AudioFileDTO(
            id=row.id,
            file_name=row.file_name,
            file_path=row.file_path,
            uploaded_at=row.uploaded_at,
        )
