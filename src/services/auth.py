from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException
from jwt.exceptions import ExpiredSignatureError
from passlib.context import CryptContext

from services.base import BaseService
from src.config import settings
from src.schemas.auth import LoginData, TokenType


class AuthService(BaseService):
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self) -> None:
        super().__init__(db_manager=None)

    def _hash_password(self, password) -> str:
        return self._pwd_context.hash(password)

    def _verify_password(self, plain_password, hashed_password) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)

    def _generate_token(
        self,
        payload: dict,
        expires_delta: timedelta,
        type: TokenType,
    ) -> str:
        token_data = payload.copy()
        now = datetime.now(timezone.utc)
        token_data["exp"] = datetime.timestamp(now + expires_delta)
        token_data["iat"] = datetime.timestamp(now)
        token_data["type"] = type

        return jwt.encode(
            payload=token_data,
            key=settings.JWT_PRIVATE_KEY.read_text(),
            algorithm=settings.JWT_ALGORITHM,
        )

    def create_access_token(self, payload: dict) -> str:
        return self._generate_token(
            payload=payload,
            expires_delta=settings.JWT_EXPIRE_DELTA_ACCESS,
            type=TokenType.ACCESS,
        )

    def create_refresh_token(self, payload: dict) -> str:
        return self._generate_token(
            payload=payload,
            expires_delta=settings.JWT_EXPIRE_DELTA_REFRESH,
            type=TokenType.REFRESH,
        )

    def decode_token(self, token: str) -> dict:
        try:
            decoded_token = jwt.decode(
                jwt=token,
                key=settings.JWT_PUBLIC_KEY.read_text(),
                algorithms=(settings.JWT_ALGORITHM),
            )
        except ExpiredSignatureError as exc:
            raise HTTPException(status_code=401, detail=str(exc))
        return decoded_token

    async def login_user(self, login_data: LoginData):
        ...

        access_token = self.create_access_token(payload={"sub": login_data.username})
        refresh_token = self.create_refresh_token(payload={"sub": login_data.username})

        return (access_token, refresh_token)
