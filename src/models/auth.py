from datetime import datetime

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base
from src.schemas.auth import TokenType


class Token(Base):
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    type: Mapped[TokenType] = mapped_column(ENUM(TokenType))
    hashed_data: Mapped[str]
    expires_at: Mapped[datetime]


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    birth_date: Mapped[datetime]
    hashed_password: Mapped[str]
    email: Mapped[str]
    bio: Mapped[str] = mapped_column(Text, nullable=True)
