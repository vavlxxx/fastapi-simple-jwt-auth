from typing import Self

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class DBManager:
    def __init__(self, session_factory: async_sessionmaker) -> None:
        self.session_factory = session_factory

    async def __aenter__(self) -> Self:
        self.session: AsyncSession = self.session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.rollback()
        await self.session.close()

    async def check_connection(self) -> None:
        await self.session.execute(text("SELECT version();"))

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
