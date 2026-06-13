import uuid

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.categories import CategoryCreate, CategoryResponse
from src.core.db import get_db

from src.api.routes.depends import (
    create_category_use_case,
    get_category_by_id_use_case,
    get_category_by_title_use_case,
)

from src.domain.categories.use_cases.create_category import CreateCategoryUseCase
from src.domain.categories.use_cases.get_category import (
    GetCategoryByIdUseCase,
    GetCategoryByTitleUseCase,
)

from src.core.exceptions.domain_exceptions import (
    CategoryAlreadyExistsException,
    CategoryNotFoundByIdException,
    CategoryNotFoundByTitleException,
    UserNotFoundByIdException,
    UserDoingForbiddenActions,
)

from src.services.auth import AuthService
from src.schemas.users import UserResponse

router = APIRouter()


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=CategoryResponse)
async def get_category_by_id(
    id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    use_case: GetCategoryByIdUseCase = Depends(get_category_by_id_use_case),
) -> CategoryResponse:
    try:
        category = await use_case.execute(session=session, id=id)
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )

    return category


@router.get(
    "/title/{title}", status_code=status.HTTP_200_OK, response_model=CategoryResponse
)
async def get_category_by_title(
    title: str,
    session: AsyncSession = Depends(get_db),
    use_case: GetCategoryByTitleUseCase = Depends(get_category_by_title_use_case),
) -> CategoryResponse:
    try:
        category = await use_case.execute(session=session, title=title)
    except CategoryNotFoundByTitleException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )

    return category


@router.post(
    "/create",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    category_create: CategoryCreate,
    session: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(AuthService.get_current_user),
    use_case: CreateCategoryUseCase = Depends(create_category_use_case),
) -> CategoryResponse:
    try:
        category = await use_case.execute(
            current_user=current_user, session=session, category_create=category_create
        )
        return category

    except CategoryAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail()
        )
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.get_detail()
        )
    except UserDoingForbiddenActions as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.get_detail()
        )
