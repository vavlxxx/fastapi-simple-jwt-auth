from datetime import datetime
from enum import Enum

from pydantic import Field

from src.schemas.base import BaseDTO


class UserLoginDTO(BaseDTO):
    username: str = Field("admin123", min_length=8, max_length=32)
    password: str = Field("admin123", min_length=8)


class UserRegisterDTO(UserLoginDTO):
    username: str = Field("admin123", min_length=8, max_length=32)
    password: str = Field("admin123", min_length=8)


class UserAddDTO(BaseDTO):
    username: str
    hashed_password: str


class UserDTO(BaseDTO):
    id: int
    username: str = Field(..., min_length=8, max_length=32)
    first_name: str | None = Field(None, min_length=1, max_length=150)
    last_name: str | None = Field(None, min_length=1, max_length=150)


class UserUpdateDTO(BaseDTO):
    first_name: str | None = None
    last_name: str | None = None


class UserWithPasswordDTO(UserDTO):
    hashed_password: str


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class CreatedTokenDTO(BaseDTO):
    type: TokenType
    token: str
    expires_at: datetime


class TokenAddDTO(BaseDTO):
    user_id: int
    type: TokenType
    hashed_data: str
    expires_at: datetime


class TokenDTO(TokenAddDTO):
    id: int


class TokenResponseDTO(BaseDTO):
    access_token: str
    refresh_token: str
    type: str = "Bearer"
