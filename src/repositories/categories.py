from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.categories import Category

from src.schemas.categories import CategoryCreate

from sqlalchemy.exc import IntegrityError
from src.core.exceptions.database_exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
)

from sqlalchemy import insert
from typing import Type

import uuid


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session
        self._model: Type[Category] = Category

    async def create(self, category_create: CategoryCreate) -> Category:
        query = (
            insert(self._model)
            .values(**category_create.model_dump())
            .returning(self._model)
        )
        try:
            result = await self.session.execute(query)
            created_category = result.scalar_one()
            await self.session.flush()
            return created_category

        except IntegrityError:
            await self.session.rollback()
            raise EntityAlreadyExistsException()

    async def get_by_title(self, title: str) -> Category:
        query = select(Category).where(Category.title == title)
        result = await self.session.execute(query)
        category = result.scalar_one_or_none()
        if not category:
            raise EntityNotFoundException()
        return category

    async def get_by_id(self, id: uuid.UUID) -> Category:
        query = select(Category).where(Category.id == id)
        result = await self.session.execute(query)
        category = result.scalar_one_or_none()
        if not category:
            raise EntityNotFoundException()
        return category
