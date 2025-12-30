import hashlib
from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import Response
from jwt.exceptions import DecodeError, ExpiredSignatureError

from src.config import settings
from src.schemas.auth import (
    CreatedTokenDTO,
    TokenAddDTO,
    TokenResponseDTO,
    TokenType,
    UserAddDTO,
    UserDTO,
    UserLoginDTO,
    UserRegisterDTO,
    UserUpdateDTO,
    UserWithPasswordDTO,
)
from src.services.base import BaseService
from src.utils.db_tools import DBManager
from src.utils.exceptions import (
    CannotDecodeTokenError,
    InvalidLoginDataError,
    ObjectAlreadyExistsError,
    ObjectNotFoundError,
    TokenExipedError,
    UserExistsHTTPError,
    UserNotFoundError,
)


class TokenService(BaseService):
    def __init__(self, db: DBManager | None = None) -> None:
        super().__init__(db=db)

    def hash_token(self, token: str) -> str:
        token_bytes = token.encode("utf-8")
        return hashlib.sha256(token_bytes).hexdigest()

    def verify_token(self, token: str, hashed_token: str) -> bool:
        return self.hash_token(token) == hashed_token

    def hash_pwd(self, password: str) -> str:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode(encoding="utf-8")
        hashed_pwd_bytes = bcrypt.hashpw(pwd_bytes, salt)
        return hashed_pwd_bytes.decode(encoding="utf-8")

    def verify_pwd(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode(encoding="utf-8"),
            hashed_password=hashed_password.encode(encoding="utf-8"),
        )

    def _generate_token(
        self,
        payload: dict,
        expires_delta: timedelta,
        type: TokenType,
    ) -> CreatedTokenDTO:
        token_data = payload.copy()
        now = datetime.now()
        expires = now + expires_delta
        expires_timestamp = datetime.timestamp(expires)

        token_data["exp"] = expires_timestamp
        token_data["iat"] = datetime.timestamp(now)
        token_data["type"] = type

        token = jwt.encode(
            payload=token_data,
            key=settings.auth.JWT_PRIVATE_KEY.read_text(),
            algorithm=settings.auth.JWT_ALGORITHM,
        )

        return CreatedTokenDTO(
            token=token,
            expires_at=expires,
            type=type,
        )

    def create_access_token(self, payload: dict) -> CreatedTokenDTO:
        return self._generate_token(
            payload=payload,
            expires_delta=settings.auth.JWT_EXPIRE_DELTA_ACCESS,
            type=TokenType.ACCESS,
        )

    def create_refresh_token(self, payload: dict) -> CreatedTokenDTO:
        return self._generate_token(
            payload=payload,
            expires_delta=settings.auth.JWT_EXPIRE_DELTA_REFRESH,
            type=TokenType.REFRESH,
        )

    def decode_token(self, token: str) -> dict:
        try:
            decoded_token = jwt.decode(
                jwt=token,
                key=settings.auth.JWT_PUBLIC_KEY.read_text(),
                algorithms=[settings.auth.JWT_ALGORITHM],
            )
        except ExpiredSignatureError as exc:
            raise TokenExipedError from exc
        except DecodeError as exc:
            raise CannotDecodeTokenError from exc
        return decoded_token

    async def update_tokens(
        self,
        response: Response,
        uid: int | None = None,
        user: UserDTO | UserWithPasswordDTO | None = None,  # pyright: ignore
    ) -> TokenResponseDTO:
        if user is None:
            user: UserWithPasswordDTO = await self.db.auth.get_one(id=uid)  # pyright: ignore

        access_token = self.create_access_token(payload={"username": user.username, "sub": f"{user.id}"})
        refresh_token = self.create_refresh_token(payload={"sub": f"{user.id}"})

        hashed_refresh_token = self.hash_token(refresh_token.token)

        token_to_update = TokenAddDTO(
            hashed_data=hashed_refresh_token,
            user_id=user.id,
            **refresh_token.model_dump(exclude={"token"}),
        )
        await self.db.tokens.delete(
            user_id=user.id,
            ensure_existence=False,
        )
        await self.db.tokens.add(token_to_update)
        await self.db.commit()

        response.set_cookie(
            key=settings.auth.REFRESH_TOKEN_COOKIE_KEY,
            value=refresh_token.token,
            httponly=True,
        )

        return TokenResponseDTO(
            access_token=access_token.token,
            refresh_token=refresh_token.token,
        )

    async def delete_tokens(self, uid: int) -> None:
        await self.db.tokens.delete(
            user_id=uid,
            ensure_existence=False,
        )
        await self.db.commit()


class AuthService(BaseService):
    def __init__(self, db: DBManager | None = None) -> None:
        super().__init__(db=db)

    async def login_user(self, login_data: UserLoginDTO, response: Response) -> TokenResponseDTO:
        try:
            user: UserWithPasswordDTO = await self.db.auth.get_user_with_passwd(username=login_data.username)
        except ObjectNotFoundError as exc:
            raise InvalidLoginDataError from exc

        token_service = TokenService(self.db)
        is_same = token_service.verify_pwd(login_data.password, user.hashed_password)
        if not user or not is_same:
            raise InvalidLoginDataError

        return await token_service.update_tokens(user=user, response=response)

    async def register_user(self, register_data: UserRegisterDTO) -> UserDTO:
        hashed_password = TokenService(self.db).hash_pwd(register_data.password)
        user_to_add = UserAddDTO(
            hashed_password=hashed_password,
            **register_data.model_dump(exclude={"password"}),
        )
        try:
            user = await self.db.auth.add(user_to_add)
        except ObjectAlreadyExistsError as exc:
            raise UserExistsHTTPError from exc
        await self.db.commit()
        return user

    async def get_profile(self, uid: int) -> UserDTO:
        try:
            return await self.db.auth.get_user_with_passwd(id=uid)
        except ObjectNotFoundError as exc:
            raise UserNotFoundError from exc

    async def update_profile(self, uid: int, data: UserUpdateDTO) -> UserDTO:
        await self.db.auth.edit(id=uid, data=data, ensure_existence=False)  # pyright: ignore
        await self.db.commit()
        return await self.db.auth.get_one(id=uid)
