import uuid

from fastapi import APIRouter, Depends,  status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.categories import CategoryCreate, CategoryResponse
from core.db import database

from api.routes.depends import create_category_use_case, get_category_by_id_use_case


from domain.categories.use_cases.create_category import CreateCategoryUseCase
from domain.categories.use_cases.get_category_by_id import GetCategoryByIdUseCase
router = APIRouter()


async def get_db():
    async with database.session() as session:
        yield session


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=CategoryResponse)
async def get_category_by_id(
    id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    use_case: GetCategoryByIdUseCase = Depends(get_category_by_id_use_case)
) -> CategoryResponse:
    category = await use_case.execute(session=session, id=id)
    return category


@router.post(
    "/create", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED
)
async def create_category(
        category_in: CategoryCreate,
        session: AsyncSession = Depends(get_db),
        use_case: CreateCategoryUseCase = Depends(create_category_use_case)) -> CategoryResponse:
    user = await use_case.execute(session=session, category_in=category_in)
    return user
