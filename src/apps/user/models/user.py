from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.libs.base_model import Base


class UserModel(Base):
    """User Model

    :param id: identifier
    :param name: user name
    :param surname: user surname
    :param email: user email
    :param password: user password hash
    """
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(20))
    surname: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str]

    is_admin: Mapped[bool] = mapped_column(Boolean)
