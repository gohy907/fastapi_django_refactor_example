import uuid
from typing import Optional

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.categories import Category
from repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
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

    async def does_category_exist(self, title: str) -> bool:
        query = select(Category).where(
            Category.title == title)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None
