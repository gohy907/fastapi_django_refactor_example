import uuid

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.categories import CategoryCreate, CategoryResponse
from src.core.db import get_db

from src.api.routes.depends import create_category_use_case, get_category_by_id_use_case

from src.domain.categories.use_cases.create_category import CreateCategoryUseCase
from src.domain.categories.use_cases.get_category import (
    GetCategoryByIdUseCase,
)

from src.core.exceptions.database_exceptions import CategoryAlreadyExistsException

from src.services.auth import AuthService
from src.schemas.users import UserResponse

router = APIRouter()


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=CategoryResponse)
async def get_category_by_id(
    id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    use_case: GetCategoryByIdUseCase = Depends(get_category_by_id_use_case),
) -> CategoryResponse:
    category = await use_case.execute(session=session, id=id)
    return category


@router.post(
    "/create",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    category_in: CategoryCreate,
    session: AsyncSession = Depends(get_db),
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case: CreateCategoryUseCase = Depends(create_category_use_case),
) -> CategoryResponse:
    try:
        user = await use_case.execute(session=session, category_in=category_in)
        return user

    except CategoryAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail()
        )
    return user
