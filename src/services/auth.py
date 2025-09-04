from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException
from jwt.exceptions import ExpiredSignatureError
from passlib.context import CryptContext

from src.config import settings
from src.schemas.auth import (
    CreatedTokenDTO,
    LoginData,
    TokenAddDTO,
    TokenResponseDTO,
    TokenType,
)
from src.services.base import BaseService
from src.utils.db_manager import DBManager
from src.utils.exceptions import InvalidLoginDataError


class AuthService(BaseService):
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, db_manager: DBManager | None = None) -> None:
        super().__init__(db_manager=db_manager)

    def _hash_data(self, password) -> str:
        return self._pwd_context.hash(password)

    def _verify_data(self, plain_password, hashed_password) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)

    def _generate_token(
        self,
        payload: dict,
        expires_delta: timedelta,
        type: TokenType,
    ) -> CreatedTokenDTO:
        token_data = payload.copy()
        now = datetime.now(timezone.utc)
        expires = now + expires_delta
        expires_timestamp = datetime.timestamp(expires)

        token_data["exp"] = expires_timestamp
        token_data["iat"] = datetime.timestamp(now)
        token_data["type"] = type

        token = jwt.encode(
            payload=token_data,
            key=settings.JWT_PRIVATE_KEY.read_text(),
            algorithm=settings.JWT_ALGORITHM,
        )

        return CreatedTokenDTO(
            token=token,
            expires_at=expires,
            type=type,
        )

    def create_access_token(self, payload: dict) -> CreatedTokenDTO:
        return self._generate_token(
            payload=payload,
            expires_delta=settings.JWT_EXPIRE_DELTA_ACCESS,
            type=TokenType.ACCESS,
        )

    def create_refresh_token(self, payload: dict) -> CreatedTokenDTO:
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
        hashed_password = self._hash_data(login_data.password)
        user = await self.db.auth.get_user_with_passwd(username=login_data.username)

        is_same = self._verify_data(hashed_password, user.hashed_password)
        if not user or not is_same:
            raise InvalidLoginDataError

        access_token = self.create_access_token(
            payload={"sub": login_data.username, "uid": user.id}
        )
        refresh_token = self.create_refresh_token(payload={"sub": login_data.username})
        hashed_refresh_token = self._hash_data(refresh_token)

        data_to_add = TokenAddDTO(
            hashed_data=hashed_refresh_token,
            **refresh_token.model_dump(exclude={"token"}),
        )
        await self.db.tokens.delete(owner_id=user.id)
        await self.db.tokens.add(data_to_add)
        await self.db.commit()

        return TokenResponseDTO(
            access_token=access_token.token,
            refresh_token=refresh_token.token,
        )
