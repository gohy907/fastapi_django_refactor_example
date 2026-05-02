from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.schemas.users import CreateUser, UserInternal

from src.models.users import User as UserModel
from src.core.exceptions.database_exceptions import UserNotFoundException, UserAlreadyExistsException

from typing import Type

from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from src.resources import get_password_hash


class UserRepository:
    def __init__(self):
        self._model: Type[UserModel] = UserModel

    def get(self, session: Session, login: str) -> UserInternal | None:
        query = (
            select(self._model)
            .where(self._model.login == login)
        )

        user = session.scalar(query)
        if not user:
            raise UserNotFoundException()

        return user

    async def create(self, session: AsyncSession, user_create: CreateUser) -> UserModel:

        user_data = user_create.model_dump(exclude={"password"})
        user_data["password_hash"] = get_password_hash(user_create.password)

        query = (
            insert(self._model)
            .values(**user_data)
            .returning(self._model)
        )

        try:
            result = await session.execute(query)
            created_user = result.scalar_one()
            await session.flush()
            return created_user

        except IntegrityError:
            await session.rollback()
            raise UserAlreadyExistsException()
