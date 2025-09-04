from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends

from src.db import sessionmaker
from src.utils.db_manager import DBManager


async def get_db() -> AsyncGenerator[DBManager, Any]:
    async with DBManager(session_factory=sessionmaker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
