from typing import List, Type, Optional
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError

from src.apps.audio.entity import AudioFileEntity
from src.config.database.session import ISession
from src.apps.audio.models.audio_file import AudioFileModel
from src.apps.audio.dto import AudioFileDTO

from src.libs.exceptions import AlreadyExistError

class AudioFileRepository:
    model: Type[AudioFileModel] = AudioFileModel

    def __init__(self, session: ISession) -> None:
        self.session: ISession = session

    async def create(self, audio_file: AudioFileEntity) -> AudioFileDTO:
        instance: AudioFileModel = AudioFileModel(**audio_file.__dict__)
        self.session.add(instance)
        try:
            await self.session.commit()
        except IntegrityError:
            raise AlreadyExistError(f'{instance.file_name} is already exist')
        await self.session.refresh(instance)
        return self._get_dto(instance)

    async def get(self, pk: int) -> Optional[AudioFileDTO]:
        stmt = select(self.model).filter_by(id=pk)
        result: Optional[AudioFileModel] = (await self.session.execute(stmt)).scalar_one_or_none()
        return self._get_dto(result) if result is not None else None

    async def get_by_user(self, user_id: int) -> List[AudioFileDTO]:
        stmt = select(self.model).filter_by(user_id=user_id)
        results: List[AudioFileModel] = (await self.session.execute(stmt)).scalars().all()
        return [self._get_dto(row) for row in results]

    async def delete(self, pk: int) -> None:
        stmt = delete(self.model).where(self.model.id == pk)
        await self.session.execute(stmt)
        await self.session.commit()

    def _get_dto(self, row: AudioFileModel) -> AudioFileDTO:
        return AudioFileDTO(
            id=row.id,
            file_name=row.file_name,
            file_path=row.file_path,
            file_description=row.file_description,
            file_size=row.file_size,
            user_id=row.user_id
        )
