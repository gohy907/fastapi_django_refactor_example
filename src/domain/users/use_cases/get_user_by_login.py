import logging

from src.core.db import database
from src.repositories.users import UserRepository
from src.schemas.users import UserResponse
from src.core.exceptions.database_exceptions import EntityNotFoundException
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class GetUserByLoginUseCase:
    def __init__(self):
        self._database = database

    async def execute(
        self, session: AsyncSession, login: str, current_user: UserResponse
    ) -> UserResponse:

        repo = UserRepository(session)
        try:
            user = await repo.get_by_login(login=login)
        except EntityNotFoundException:
            error = UserNotFoundByLoginException(login=login)
            logger.error(
                f"Пользователь {current_user.login} довел приложение до ошибки: {
                    error.get_detail()
                }"
            )
            raise error

        user = UserResponse.model_validate(obj=user)
        return user
