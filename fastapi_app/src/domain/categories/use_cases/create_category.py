from fastapi import HTTPException, status
from src.repositories.categories import CategoryRepository
from src.schemas.categories import CategoryResponse, CategoryCreate

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.users.use_cases.get_user_by_id import GetUserByIdUseCase
from src.domain.categories.use_cases.get_category import GetCategoryByTitleUseCase


class CreateCategoryUseCase:

    def __init__(self):
        pass

    async def execute(self, session: AsyncSession, category_in: CategoryCreate) -> CategoryResponse:
        repo = CategoryRepository(session)
        category_data = category_in.model_dump()
        category = await repo.create(category_data)
        await session.commit()

        return CategoryResponse.model_validate(category)
