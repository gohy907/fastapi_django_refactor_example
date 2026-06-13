import uuid
from src.repositories.users import UserRepository

from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.users import UserUpdate, UserResponse
from src.core.exceptions.database_exceptions import EntityAlreadyExistsException
from src.core.exceptions.domain_exceptions import (
    UserAlreadyExistsException,
    UserUpdatingWithoutAuth,
)
from src.domain.users.use_cases.get_user_by_id import GetUserByIdUseCase

import logging

logger = logging.getLogger(__name__)


class UpdateUserUseCase:
    def __init__(self, get_user_use_case: GetUserByIdUseCase):
        self._get_user_use_case = get_user_use_case

    async def execute(
        self,
        session: AsyncSession,
        id: uuid.UUID,
        current_user: UserResponse,
        user_update: UserUpdate,
    ) -> UserResponse:

        if current_user.id != id:
            error = UserUpdatingWithoutAuth()

            logger.error(
                f"Пользователь с id {
                    current_user.id
                } попытался отредактировать пользователя с id {id}: {
                    error.get_detail()
                }"
            )
            raise error

        repo = UserRepository(session)
        try:
            updated_user = await repo.update(
                id=id, user_update=user_update.to_internal()
            )
        except EntityAlreadyExistsException:
            logger.info(f"User {user_update.login} already exists, aborting creation")
            error = UserAlreadyExistsException(login=user_update.login)
            logger.error(
                f"Пользователь {current_user.login} довел приложение до ошибки: {
                    error.get_detail()
                }"
            )
            raise error

        await session.flush()

        user = UserResponse.model_validate(obj=updated_user)
        return user
