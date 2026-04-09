import uuid

from repositories.categories import CategoryRepository
from schemas.categories import CategoryResponse
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession


class GetCategoryByIdUseCase:

    def __init__(self):
        pass

    async def execute(self, session: AsyncSession, id: uuid.UUID) -> CategoryResponse:
        repo = CategoryRepository(session)
        return CategoryResponse.model_validate(category)


class GetCategoryByTitleUseCase:
    def __init__(self):
        pass

    async def execute(self, session: AsyncSession, title: str) -> CategoryResponse:
        repo = CategoryRepository(session)

        category = await repo.get_by_title(title)
        return CategoryResponse.model_validate(category)
