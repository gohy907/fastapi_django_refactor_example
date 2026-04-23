import logging

from core.db import database
from repositories.users import UserRepository
from schemas.users import UserResponse as UserSchema
from resources.auth import verify_password
from core.exceptions.database_exceptions import UserNotFoundException
from core.exceptions.domain_exceptions import UserNotFoundByLoginException, WrongPasswordException
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class AuthenticateUserUseCase:
    def __init__(self) -> None:
        pass

    async def execute(
        self,
        login: str,
        password: str,
        session: AsyncSession,
    ) -> UserSchema:
        repo = UserRepository()
        try:
            user = await repo.get(session=session, login=login)
        except UserNotFoundException:
            error = UserNotFoundByLoginException(session=session, login=login)
            logger.error(error.get_detail())
            raise error

        if not verify_password(plain_password=password, hashed_password=user.password_hash):
            error = WrongPasswordException()
            logger.error(error.get_detail())
            raise error

        return UserSchema.model_validate(obj=user)
