import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI

from src.api import router as main_router
from src.config import settings

app = FastAPI(
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
