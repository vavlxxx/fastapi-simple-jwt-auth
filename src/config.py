from datetime import timedelta
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_NAME: str
    DB_PORT: int
    DB_PASSWORD: str
    DB_ECHO: bool = False

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    UVICORN_PORT: int = 8000
    UVICORN_HOST: str = "127.0.0.1"
    UVICORN_RELOAD: bool = True

    JWT_EXPIRE_DELTA_ACCESS: timedelta = timedelta(minutes=5)
    JWT_EXPIRE_DELTA_REFRESH: timedelta = timedelta(days=7)
    JWT_ALGORITHM: str = "RS256"
    JWT_PRIVATE_KEY: Path = BASE_DIR / "creds" / "jwt-private.pem"
    JWT_PUBLIC_KEY: Path = BASE_DIR / "creds" / "jwt-public.pem"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


settings = Settings()  # type: ignore
