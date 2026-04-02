from repositories.categories import CategoryRepository
from schemas.categories import CategoryResponse, CategoryCreate

from sqlalchemy.ext.asyncio import AsyncSession

from domain.users.use_cases.get_user_by_id import GetUserByIdUseCase


class CreateCategoryUseCase:

    def __init__(self):

        self.get_user_use_case = GetUserByIdUseCase()
        pass

    async def execute(self, session: AsyncSession, category_in: CategoryCreate) -> CategoryResponse:
        repo = CategoryRepository(session)

        await self.get_user_use_case.execute(session, category_in.author_id)

        category_data = category_in.model_dump()
        category = await repo.create(category_data)
        await session.commit()

        return CategoryResponse.model_validate(category)
