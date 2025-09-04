from src.models.auth import User
from src.repos.mappers.base import DataMapper
from src.schemas.auth import UserDTO


class AuthMapper(DataMapper[User, UserDTO]): ...
