from fastapi import APIRouter

from src.api.v1.dependencies.auth import UserDataByAccess, UserDataByRefresh
from src.api.v1.dependencies.db import DBDep
from src.schemas.auth import LoginData, RegisterData, TokenResponseDTO
from src.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication and Authorization"],
)


@router.post("/login/")
async def login(
    db: DBDep,
    login_data: LoginData,
) -> TokenResponseDTO:
    """
    Login user
    """
    return await AuthService(db).login_user(login_data=login_data)


@router.post("/register/")
async def register(
    db: DBDep,
    register_data: RegisterData,
):
    """
    Register user
    """
    return await AuthService(db).register_user(register_data=register_data)


@router.get("/profile/")
async def get_profile(userdata: UserDataByAccess):
    """
    User's profile
    """
    return userdata


@router.get("/refresh/")
async def refresh(userdata: UserDataByRefresh):
    """
    Refresh token
    """
    access_token, refresh_token = (..., ...)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
