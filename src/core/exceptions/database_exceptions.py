class BaseDatabaseException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail or "An error occurred"


class EntityNotFoundException(BaseDatabaseException):
    pass


class EntityAlreadyExistsException(BaseDatabaseException):
    pass


class DatabaseError(BaseDatabaseException):
    pass
