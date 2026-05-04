import logging

from src.repositories.users import UserRepository
from src.schemas.users import UserResponse as UserSchema
from src.resources.auth import verify_password
from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException, WrongPasswordException
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
            user = await repo.get_by_login(session=session, login=login)
        except UserNotFoundException:
            error = UserNotFoundByLoginException(
                login=login)
            logger.error(error.get_detail())
            raise error

        if not verify_password(plain_password=password, hashed_password=user.password_hash):
            error = WrongPasswordException()
            logger.error(error.get_detail())
            raise error

        return UserSchema.model_validate(obj=user)
