from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from pydantic import SecretStr
from jose import JWTError, jwt

from src.core.exceptions.auth_exceptions import CredentialsException
from src.core.exceptions.database_exceptions import EntityNotFoundException
from src.schemas.users import UserResponse
from src.resources.auth import oauth2_scheme
from src.core.db import get_db
from src.repositories.users import UserRepository

AUTH_EXCEPTION_MESSAGE = "Невозможно проверить данные авторизации"
SECRET_AUTH_KEY = SecretStr(
    "aF75A92Cd9s10KGL4nLdt1r85XRtZ7APNO6NheGeKdRBhhc9oObQywxmqPF"
)
AUTH_ALGORITHM = "HS256"


class AuthService:
    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(get_db),
    ):
        _repo: UserRepository = UserRepository()

        try:
            payload = jwt.decode(
                token=token,
                key=SECRET_AUTH_KEY.get_secret_value(),
                algorithms=[AUTH_ALGORITHM],
            )
            username: str = payload.get("sub")
            if username is None:
                raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)
        except JWTError:
            raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)

        try:
            user = await _repo.get_by_login(session=session, login=username)
        except EntityNotFoundException:
            raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)

        return UserResponse.model_validate(obj=user)
