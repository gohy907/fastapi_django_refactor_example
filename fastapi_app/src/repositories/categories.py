from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.categories import Category
from repositories.base import BaseRepository

from sqlalchemy.exc import IntegrityError
from core.exceptions import CategoryAlreadyExistsError, UserDoesNotExist


class CategoryRepository(BaseRepository[Category]):


    async def create(self, data: dict) -> Category:
            try:
                return await super().create(data)
            except IntegrityError as e:
                error_msg = str(e.orig).lower()
                if "foreign key" in error_msg or "is not present in table" in error_msg:
                    raise UserDoesNotExist()

                if "already exists" in error_msg or "duplicate key" in error_msg or "unique constraint" in error_msg:
                    raise CategoryAlreadyExistsError()

                raise e

    def __init__(self, session: AsyncSession):
        super().__init__(Category, session)

    async def get_by_title(self, title: str) -> Optional[Category]:
        query = select(Category).where(Category.title == title)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
