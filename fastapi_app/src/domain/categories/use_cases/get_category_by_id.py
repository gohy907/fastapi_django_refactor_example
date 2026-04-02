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

        category = await repo.get(id)

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        return CategoryResponse.model_validate(category)
