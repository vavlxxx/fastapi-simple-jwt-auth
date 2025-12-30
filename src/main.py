import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

sys.path.append(str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI

from src.api import router as main_router
from src.config import settings
from src.db import engine
from src.utils.db_tools import DBHealthChecker
from src.utils.logging import configurate_logging, get_logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger = get_logger("src")

    await DBHealthChecker(engine=engine).check()

    logger.info("All checks passed!")
    yield
    logger.info("Shutting down...")


configurate_logging()
app = FastAPI(
    lifespan=lifespan,
    title=settings.app.TITLE,
)
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.uvicorn.UVICORN_HOST,
        port=settings.uvicorn.UVICORN_PORT,
        reload=settings.uvicorn.UVICORN_RELOAD,
    )
