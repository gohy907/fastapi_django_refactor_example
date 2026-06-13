from src.repositories.categories import CategoryRepository
from src.repositories.users import UserRepository

from src.schemas.categories import CategoryResponse, CategoryCreate

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.database_exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
)
from src.core.exceptions.domain_exceptions import (
    CategoryAlreadyExistsException,
    UserNotFoundByIdException,
)

import logging

logger = logging.getLogger(__name__)


class CreateCategoryUseCase:
    def __init__(self):
        pass

    async def execute(
        self, session: AsyncSession, category_in: CategoryCreate
    ) -> CategoryResponse:
        user_repo = UserRepository(session)
        try:
            await user_repo.get_by_id(category_in.author_id)
        except EntityNotFoundException:
            raise UserNotFoundByIdException(id=category_in.author_id)

        category_repo = CategoryRepository(session)
        try:
            category = await category_repo.create(category_in)

        except EntityAlreadyExistsException:
            logger.info(
                f"Category {category_in.title} already exists, aborting creation"
            )
            raise CategoryAlreadyExistsException(title=category_in.title)
        await session.commit()

        return CategoryResponse.model_validate(category)
