class BaseDatabaseException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail or "An error occurred"


class UserNotFoundException(BaseDatabaseException):
    pass


class CategoryNotFoundException(BaseDatabaseException):
    pass


class PostNotFoundException(BaseDatabaseException):
    pass


class UserAlreadyExistsException(BaseDatabaseException):
    pass


class CategoryAlreadyExistsException(BaseDatabaseException):
    pass


class PostAlreadyExistsException(BaseDatabaseException):
    pass
