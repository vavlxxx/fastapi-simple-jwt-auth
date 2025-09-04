class ApplicationBaseError(Exception):
    detail = "Something went wrong"

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class ObjectNotFoundError(ApplicationBaseError):
    detail = "Object not found"


class ObjectAlreadyExistsError(ApplicationBaseError):
    detail = "Object already exists"


class ValueOutOfRangeError(ApplicationBaseError):
    detail = "Value out of integer range"


class InvalidLoginDataError(ApplicationBaseError):
    detail = "Invalid login data, wrong password or username"
