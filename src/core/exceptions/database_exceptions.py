class BaseDatabaseException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail


class UserNotFoundException(BaseDatabaseException):
    pass


class PostNotFoundException(BaseDatabaseException):
    pass


class UserAlreadyExistsException(BaseDatabaseException):
    pass


class PostAlreadyExistsException(BaseDatabaseException):
    pass
