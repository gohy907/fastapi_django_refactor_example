import logging
import uuid

from src.core.db import database
from src.repositories.users import UserRepository
from src.schemas.users import UserResponse
from src.core.exceptions.database_exceptions import EntityNotFoundException
from src.core.exceptions.domain_exceptions import UserNotFoundByIdException
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class GetUserByIdUseCase:
    def __init__(self):
        self._database = database

    async def execute(
        self, session: AsyncSession, id: uuid.UUID, current_user: UserResponse
    ) -> UserResponse:

        repo = UserRepository(session)
        try:
            user = await repo.get_by_id(id=id)
        except EntityNotFoundException:
            error = UserNotFoundByIdException(id=id)
            logger.error(
                f"Пользователь {current_user.login} довел приложение до ошибки: {
                    error.get_detail()
                }"
            )
            raise error
        except Exception as e:
            logger.error(
                f"Пользователь {current_user.login} довел приложение до ошибки: {
                    e.get_detail()
                }"
            )
            raise e

        user = UserResponse.model_validate(obj=user)
        return user
