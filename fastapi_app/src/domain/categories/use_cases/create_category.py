from fastapi import HTTPException, status
from repositories.categories import CategoryRepository
from schemas.categories import CategoryResponse, CategoryCreate

from sqlalchemy.ext.asyncio import AsyncSession

from domain.users.use_cases.get_user_by_id import GetUserByIdUseCase
from domain.categories.use_cases.get_category import GetCategoryByTitleUseCase


class CreateCategoryUseCase:

    def __init__(self):
        self.get_category_by_title_use_case = GetCategoryByTitleUseCase()
        self.get_user_use_case = GetUserByIdUseCase()
        pass

    async def execute(self, session: AsyncSession, category_in: CategoryCreate) -> CategoryResponse:
        repo = CategoryRepository(session)

        await self.get_user_use_case.execute(session, category_in.author_id)

        existing_category = await self.get_category_by_title_use_case.execute(
            session,
            category_in.title
        )

        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with title '{
                    category_in.title}' already exists"
            )

        category_data = category_in.model_dump()
        category = await repo.create(category_data)
        await session.commit()

        return CategoryResponse.model_validate(category)
