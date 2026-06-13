import uuid


class BaseDomainException(Exception):
    def __init__(self, detail: str) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail


class UserNotFoundByLoginException(BaseDomainException):
    _exception_text_template = "Пользователь с логином='{login}' не найден"

    def __init__(self, login: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            login=login
        )

        super().__init__(detail=self._exception_text_template)


class UserNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Пользователь с id='{id}' не найден"

    def __init__(self, id: uuid.UUID) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)

        super().__init__(detail=self._exception_text_template)


class UserAlreadyExistsException(BaseDomainException):
    _exception_text_template = "Пользователь с логином='{login}' уже существует"

    def __init__(self, login: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            login=login
        )

        super().__init__(detail=self._exception_text_template)


class WrongPasswordException(BaseDomainException):
    _exception_text = "Неверный пароль"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text)


class UserUpdatingWithoutAuth(BaseDomainException):
    _exception_text: str = "Недостаточно прав для изменения профиля"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text)


class CategoryAlreadyExistsException(BaseDomainException):
    _exception_text_template = "Категория с названием='{title}' уже существует"

    def __init__(self, title: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            title=title
        )
        super().__init__(detail=self._exception_text_template)


class CategoryNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Категория с id='{id}' не найдена"

    def __init__(self, id: uuid.UUID) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)
        super().__init__(detail=self._exception_text_template)


class CategoryNotFoundByTitleException(BaseDomainException):
    _exception_text_template = "Категория с названием='{title}' не найдена"

    def __init__(self, title: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            title=title
        )
        super().__init__(detail=self._exception_text_template)


class DatabaseError(BaseDomainException):
    _exception_text_template = "Database error: {message}"

    def __init__(self, message: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            message=message
        )
        super().__init__(detail=self._exception_text_template)
