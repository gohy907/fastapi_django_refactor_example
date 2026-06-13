from src.repositories.users import UserRepository

from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.users import UserCreate, UserResponse
from src.core.db import database
from src.core.exceptions.database_exceptions import EntityAlreadyExistsException
from src.core.exceptions.domain_exceptions import UserAlreadyExistsException


import logging

logger = logging.getLogger(__name__)


class CreateUserUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, session: AsyncSession, user_in: UserCreate) -> UserResponse:
        repo = UserRepository()

        try:
            user = await repo.create(session=session, user_create=user_in.to_internal())

            await session.commit()

            logger.info(f"User {user.login} has been created")
            return UserResponse.model_validate(user)
        except EntityAlreadyExistsException:
            logger.info(f"User {user_in.login} already exists, aborting creation")
            raise UserAlreadyExistsException(login=user_in.login)
