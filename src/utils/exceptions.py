from fastapi import HTTPException, status


class ApplicationError(Exception):
    detail = "Something went wrong"

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class ObjectInvalidValueError(ApplicationError):
    detail = "Object invalid value"


class ObjectNotFoundError(ApplicationError):
    detail = "Object not found"


class RelatedObjectExistsError(ApplicationError):
    detail = "Related object already exists"


class ObjectAlreadyExistsError(ApplicationError):
    detail = "Object already exists"


class ValueOutOfRangeError(ApplicationError):
    detail = "Value out of integer range"


class InvalidLoginDataError(ApplicationError):
    detail = "Invalid login data, wrong password or username"


class UserNotFoundError(ApplicationError):
    detail = "User not found"


class UserExistsError(ApplicationError):
    detail = "User already exists"


class ApplicationHTTPError(HTTPException):
    detail = "Something went wrong"
    status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail
        super().__init__(detail=self.detail, status_code=self.status)


class ExpiredSignatureHTTPError(ApplicationHTTPError):
    detail = "Token has expired, try to login again"
    status = status.HTTP_401_UNAUTHORIZED


class InvalidTokenTypeHTTPError(ApplicationHTTPError):
    detail = "Invalid token type, expected {1}, got {2}"
    status = status.HTTP_422_UNPROCESSABLE_ENTITY

    def __init__(self, *args, expected_type, actual_type, **kwargs):
        self.detail = self.detail.format(expected_type, actual_type)
        super().__init__(*args, detail=self.detail, **kwargs)


class WithdrawnTokenHTTPError(ApplicationHTTPError):
    detail = "Withdrawn refresh token, try to login again"
    status = status.HTTP_403_FORBIDDEN


class MissingSubjectHTTPError(ApplicationHTTPError):
    detail = "Missing token subject field"
    status = status.HTTP_422_UNPROCESSABLE_ENTITY


class MissingTokenHTTPError(ApplicationHTTPError):
    detail = "Missing token"
    status = status.HTTP_401_UNAUTHORIZED


class UserNotFoundHTTPError(ApplicationHTTPError):
    detail = "User not found"
    status = status.HTTP_404_NOT_FOUND


class UserExistsHTTPError(ApplicationHTTPError):
    detail = "User already exists"
    status = status.HTTP_409_CONFLICT


class InvalidLoginDataHTTPError(ApplicationHTTPError):
    detail = "Invalid login data, wrong password or username"
    status = status.HTTP_401_UNAUTHORIZED
