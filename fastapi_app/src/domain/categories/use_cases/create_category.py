from repositories.categories import CategoryRepository
from schemas.categories import CategoryResponse, CategoryCreate

from sqlalchemy.ext.asyncio import AsyncSession


class CreateCategoryUseCase:

    def __init__(self):
        pass

    async def execute(self, session: AsyncSession, category_in: CategoryCreate) -> CategoryResponse:
        repo = CategoryRepository(session)

        category_data = category_in.model_dump()
        category = await repo.create(category_data)
        await session.commit()

        return CategoryResponse.model_validate(category)
