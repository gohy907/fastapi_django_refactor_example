import uuid

from domain.users.use_cases.create_user import CreateUserUseCase
from domain.users.use_cases.get_user_by_id import GetUserByIdUseCase

from fastapi import APIRouter, Depends,  status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.users import UserCreate, UserResponse
from core.db import database

from api.routes.depends import create_user_use_case, get_user_by_id_use_case

router = APIRouter()


async def get_db():
    async with database.session() as session:
        yield session


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_by_id(
    id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    use_case: GetUserByIdUseCase = Depends(get_user_by_id_use_case)
) -> UserResponse:
    user = await use_case.execute(session=session, id=id)
    return user


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(
        user_in: UserCreate,
        session: AsyncSession = Depends(get_db),
        use_case: CreateUserUseCase = Depends(create_user_use_case)):
    user = await use_case.execute(session=session, user_in=user_in)
    return user
