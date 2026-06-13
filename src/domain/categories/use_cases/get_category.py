import uuid

from src.repositories.categories import CategoryRepository
from src.schemas.categories import CategoryResponse

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    CategoryNotFoundByTitleException,
)
from src.core.exceptions.database_exceptions import EntityNotFoundException


class GetCategoryByIdUseCase:
    def __init__(self):
        pass

    async def execute(self, session: AsyncSession, id: uuid.UUID) -> CategoryResponse:
        repo = CategoryRepository(session)
        try:
            category = await repo.get_by_id(id)
        except EntityNotFoundException:
            raise CategoryNotFoundByIdException(id=id)
        return CategoryResponse.model_validate(category)


class GetCategoryByTitleUseCase:
    def __init__(self):
        pass

    async def execute(self, session: AsyncSession, title: str) -> CategoryResponse:
        repo = CategoryRepository(session)
        try:
            category = await repo.get_by_title(title)
        except EntityNotFoundException:
            raise CategoryNotFoundByTitleException(title=title)

        return CategoryResponse.model_validate(category)
