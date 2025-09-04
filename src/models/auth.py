from datetime import datetime

from sqlalchemy.orm import Mapped

from src.models.base import Base


class Token(Base):
    hashed_data: Mapped[str]
    expires_at: Mapped[datetime]
