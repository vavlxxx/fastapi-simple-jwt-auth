from datetime import datetime
from enum import Enum
from typing import Annotated

from fastapi import Form
from pydantic import EmailStr

from src.schemas.base import BaseDTO


class UserLoginDTO(BaseDTO):
    username: str
    password: str


class UserDTO(UserLoginDTO):
    id: int
    first_name: str
    last_name: str
    birth_date: datetime
    email: EmailStr
    bio: str


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
    owner_id: int
    type: TokenType
    hashed_data: str
    expires_at: datetime


class TokenDTO(TokenAddDTO):
    id: int


class TokenResponseDTO(BaseDTO):
    access_token: str
    refresh_token: str
    type: str = "Bearer"


LoginData = Annotated[UserLoginDTO, Form()]
