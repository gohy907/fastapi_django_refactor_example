from fastapi import HTTPException, status
from src.repositories.categories import CategoryRepository
from src.schemas.categories import CategoryResponse, CategoryCreate

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.database_exceptions import EntityAlreadyExistsException
from src.core.exceptions.domain_exceptions import CategoryAlreadyExistsException

import logging

logger = logging.getLogger(__name__)


class CreateCategoryUseCase:
    def __init__(self):
        pass

    async def execute(
        self, session: AsyncSession, category_in: CategoryCreate
    ) -> CategoryResponse:
        repo = CategoryRepository(session)
        try:
            category = await repo.create(category_in)

        except EntityAlreadyExistsException:
            logger.info(
                f"Category {category_in.title} already exists, aborting creation"
            )
            raise CategoryAlreadyExistsException(title=category_in.title)
        await session.commit()

        return CategoryResponse.model_validate(category)
