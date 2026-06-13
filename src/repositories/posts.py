import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.models.posts import Post as PostModel
from src.core.exceptions.database_exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
)

from typing import Type

from sqlalchemy import insert, select, update

from src.schemas.posts import PostCreate


class PostRepository:
    def __init__(self):
        self._model: Type[PostModel] = PostModel

    async def get_by_id(self, session: AsyncSession, id: uuid.UUID) -> PostModel:
        query = select(self._model).where(self._model.id == id)
        result = await session.execute(query)
        post = result.scalar_one_or_none()
        if not post:
            raise EntityNotFoundException()
        return post

    async def create(self, session: AsyncSession, post_create: PostCreate) -> PostModel:

        query = (
            insert(self._model)
            .values(**post_create.model_dump())
            .returning(self._model)
        )

        try:
            result = await session.execute(query)
            created_post = result.scalar_one()
            await session.flush()
            return created_post

        except IntegrityError:
            await session.rollback()
            raise EntityAlreadyExistsException()
