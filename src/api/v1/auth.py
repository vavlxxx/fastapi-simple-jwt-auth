from fastapi import APIRouter, Body, Response

from src.api.v1.dependencies.auth import UidByAccess, UidByRefresh
from src.api.v1.dependencies.db import DBDep
from src.api.v1.examples.auth import get_examples_auth_post_login, get_examples_auth_put_profile
from src.api.v1.responses.auth import (
    AUTH_LOGIN_RESPONSES,
    AUTH_LOGOUT_RESPONSES,
    AUTH_PROFILE_RESPONSES,
    AUTH_REFRESH_RESPONSES,
    AUTH_REGISTER_RESPONSES,
)
from src.config import settings
from src.schemas.auth import TokenResponseDTO, UserDTO, UserLoginDTO, UserRegisterDTO, UserUpdateDTO
from src.services.auth import AuthService, TokenService
from src.utils.exceptions import (
    InvalidLoginDataError,
    InvalidLoginDataHTTPError,
    UserExistsError,
    UserExistsHTTPError,
    UserNotFoundError,
    UserNotFoundHTTPError,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication and Authorization"],
)


@router.post(
    path="/login/",
    summary="Войти в аккаунт",
    responses=AUTH_LOGIN_RESPONSES,
)
async def login(
    db: DBDep,
    response: Response,
    login_data: UserLoginDTO = Body(
        description="Данные о контактном канале",
        openapi_examples=get_examples_auth_post_login(),
    ),
):
    """
    ## 🔒 Войти в существующий акканут
    """
    try:
        token_response: TokenResponseDTO = await AuthService(db).login_user(
            login_data=login_data,
            response=response,
        )
    except InvalidLoginDataError as exc:
        raise InvalidLoginDataHTTPError from exc

    return token_response


@router.post(
    path="/register/",
    summary="Зарегистрироваться",
    responses=AUTH_REGISTER_RESPONSES,
)
async def register(
    db: DBDep,
    register_data: UserRegisterDTO = Body(
        description="Данные о контактном канале",
        openapi_examples=get_examples_auth_post_login(),
    ),
):
    """
    ## 🔒 Зарегистрировать нового пользователя
    """
    try:
        return await AuthService(db).register_user(register_data=register_data)
    except UserExistsError as exc:
        raise UserExistsHTTPError from exc


@router.get(
    path="/profile/",
    summary="Получить профиль пользователя",
    responses=AUTH_PROFILE_RESPONSES,
)
async def get_profile(
    db: DBDep,
    uid: UidByAccess,
) -> UserDTO:
    """
    ## 🔒 Профиль авторизованного пользователя
    """
    try:
        return await AuthService(db).get_profile(uid=uid)
    except UserNotFoundError as exc:
        raise UserNotFoundHTTPError from exc


@router.get(
    path="/refresh/",
    responses=AUTH_REFRESH_RESPONSES,
    summary="Получить новые Access и Refresh токены",
)
async def refresh(
    db: DBDep,
    uid: UidByRefresh,
    response: Response,
) -> TokenResponseDTO:
    """
    ## 🗝️ Получить новые Access и Refresh токены
    """
    token_response: TokenResponseDTO = await TokenService(db).update_tokens(
        uid=uid,
        response=response,
    )

    return token_response


@router.put(
    path="/profile/",
    summary="Обновить профиль пользователя",
    responses=AUTH_PROFILE_RESPONSES,
)
async def update_profile(
    db: DBDep,
    uid: UidByAccess,
    data: UserUpdateDTO = Body(
        description="Данные о контактном канале",
        openapi_examples=get_examples_auth_put_profile(),
    ),
) -> UserDTO:
    """
    ## 👤 Обновить профиль пользователя
    """
    profile = await AuthService(db).update_profile(uid=uid, data=data)
    return profile


@router.post(
    path="/logout/",
    summary="Выход из аккаунта",
    responses=AUTH_LOGOUT_RESPONSES,
)
async def logout(
    uid: UidByRefresh,
    db: DBDep,
    response: Response,
) -> dict[str, str]:
    """
    ## 🔒 Выход из аккаунта
    """
    await TokenService(db).delete_tokens(uid=uid)
    response.delete_cookie(
        settings.auth.REFRESH_TOKEN_COOKIE_KEY,
        httponly=True,
    )

    return {"detail": "Successfully logged out"}
