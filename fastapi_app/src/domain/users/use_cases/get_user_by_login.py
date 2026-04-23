import logging

from core.db import database
from repositories.users import UserRepository
from schemas.users import UserResponse
from core.exceptions.database_exceptions import UserNotFoundException
from core.exceptions.domain_exceptions import UserNotFoundByLoginException
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class GetUserByLoginUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, session: AsyncSession, login: str, current_user: UserResponse) -> UserResponse:
        try:
            user = await self._repo.get(session=session, login=login)
        except UserNotFoundException:
            error = UserNotFoundByLoginException(login=login)
            logger.error(
                f"Пользователь {current_user.login} довел приложение до ошибки: {
                    error.get_detail()}"
            )
            raise error

        user = UserResponse.model_validate(obj=user)
        return user
