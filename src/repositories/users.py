import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.schemas.users import UserCreate, UserInternal, UserResponse

from src.models.users import User as UserModel
from src.core.exceptions.database_exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
)
from src.repositories.base import BaseRepository

from typing import Type

from sqlalchemy import insert, select, update
from src.resources import get_password_hash


class UserRepository:
    def __init__(self):
        self._model: Type[UserModel] = UserModel

    async def get_by_login(self, session: AsyncSession, login: str) -> UserModel:
        query = select(self._model).where(self._model.login == login)

        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise EntityNotFoundException()

        return user

    async def get_by_id(self, session: AsyncSession, id: uuid.UUID) -> UserModel:
        query = select(self._model).where(self._model.id == id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise EntityNotFoundException()
        return user

    async def create(
        self, session: AsyncSession, user_create: UserInternal
    ) -> UserModel:

        query = (
            insert(self._model)
            .values(**user_create.model_dump())
            .returning(self._model)
        )

        try:
            result = await session.execute(query)
            created_user = result.scalar_one()
            await session.flush()
            return created_user

        except IntegrityError:
            await session.rollback()
            raise EntityAlreadyExistsException()

    async def update(
        self, session: AsyncSession, id: uuid.UUID, user_update: UserInternal
    ) -> UserModel:

        query = (
            update(self._model)
            .where(self._model.id == id)
            .values(**user_update.model_dump(exclude_unset=True))
            .returning(self._model)
        )

        try:
            result = await session.execute(query)
            updated_user = result.scalar_one()

            await session.flush()
            if not updated_user:
                raise EntityNotFoundException()
            return updated_user
        except IntegrityError:
            raise EntityAlreadyExistsException()
