from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base
from src.schemas.auth import TokenType


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, sort_order=-1)
    username: Mapped[str] = mapped_column(String(length=32), unique=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    hashed_password: Mapped[str]

    __table_args__ = (CheckConstraint("length(username) <= 32", name="username_length_check"),)


class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, sort_order=-1)
    user_id: Mapped[int] = mapped_column(ForeignKey(f"{User.__tablename__}.id"))
    type: Mapped[TokenType] = mapped_column(ENUM(TokenType))
    hashed_data: Mapped[str]
    expires_at: Mapped[datetime]
