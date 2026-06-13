from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.categories import Category
from src.repositories.base import BaseRepository

from sqlalchemy.exc import IntegrityError
from src.core.exceptions.database_exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
)

import uuid


class CategoryRepository(BaseRepository[Category]):
    async def create(self, data: dict) -> Category:
        try:
            return await super().create(data)
        except IntegrityError as e:
            error_msg = str(e.orig).lower()
            if "foreign key" in error_msg or "is not present in table" in error_msg:
                raise EntityNotFoundException

            if (
                "already exists" in error_msg
                or "duplicate key" in error_msg
                or "unique constraint" in error_msg
            ):
                raise EntityAlreadyExistsException

            # raise e

    def __init__(self, session: AsyncSession):
        super().__init__(Category, session)

    async def get_by_title(self, title: str) -> Optional[Category]:
        query = select(Category).where(Category.title == title)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id(self, id: uuid.UUID) -> Optional[Category]:
        query = select(Category).where(Category.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
