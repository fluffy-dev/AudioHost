from typing import List

from sqlalchemy import ForeignKey, String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.libs.base_model import Base


class AudioFileModel(Base):

    __tablename__ = "audio_files"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    file_name: Mapped[str] = mapped_column(String(100))
    file_path: Mapped[str] = mapped_column(Text)
    file_size: Mapped[int] = mapped_column(Integer, nullable=True)

    # Relationship: one user to many audio files
    user: Mapped[List["UserModel"]] = relationship(
        back_populates="audio_files",
    )
