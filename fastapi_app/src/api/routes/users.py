import uuid

from src.domain.users.use_cases.create_user import CreateUserUseCase
from src.domain.users.use_cases.get_user_by_id import GetUserByIdUseCase
from src.schemas.users import UserCreate, UserResponse
from fastapi import APIRouter, Depends,  status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import database

from src.api.routes.depends import create_user_use_case, get_user_by_id_use_case, get_get_user_by_login_use_case


from src.domain.users.use_cases.get_user_by_login import GetUserByLoginUseCase
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException, UserLoginIsNotUniqueException
from src.services.auth import AuthService

router = APIRouter()


async def get_db():
    async with database.session() as session:
        yield session


@router.get(
    "/{login}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def get_user_by_login(
    login: str,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case: GetUserByLoginUseCase = Depends(get_get_user_by_login_use_case),
    session: AsyncSession = Depends(get_db)
) -> UserResponse:
    try:
        return await use_case.execute(login=login, current_user=user, session=session)
    except UserNotFoundByLoginException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(
    user: UserCreate,
    use_case: CreateUserUseCase = Depends(create_user_use_case),
    session: AsyncSession = Depends(get_db)
) -> UserResponse:
    try:

        user = await use_case.execute(user_in=user, session=session)
        return user
    except UserLoginIsNotUniqueException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail())
