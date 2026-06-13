from fastapi import HTTPException, status
from src.repositories.categories import CategoryRepository
from src.schemas.categories import CategoryResponse, CategoryCreate

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.users.use_cases.get_user_by_id import GetUserByIdUseCase
from src.domain.categories.use_cases.get_category import GetCategoryByTitleUseCase

from src.core.exceptions.exc import CategoryAlreadyExistsError
from src.core.exceptions.database_exceptions import CategoryAlreadyExistsException

import logging

logger = logging.getLogger(__name__)


class CreateCategoryUseCase:
    def __init__(self):
        pass

    async def execute(
        self, session: AsyncSession, category_in: CategoryCreate
    ) -> CategoryResponse:
        repo = CategoryRepository(session)
        category_data = category_in.model_dump()
        try:
            category = await repo.create(category_data)

        except CategoryAlreadyExistsError:
            logger.info(
                f"Category {category_in.title} already exists, aborting creation"
            )
            raise CategoryAlreadyExistsException()
        await session.commit()

        return CategoryResponse.model_validate(category)
