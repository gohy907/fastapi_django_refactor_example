import uuid

from domain.users.use_cases.create_user import CreateUserUseCase
from domain.users.use_cases.get_user_by_id import GetUserByIdUseCase

from fastapi import APIRouter, Depends,  status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.users import UserCreate, UserResponse
from core.db import database

from api.routes.depends import create_user_use_case, get_user_by_id_use_case
from repositories.users import UserRepository

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
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)

    user_data = user_in.model_dump()
    password_plain = str(user_in.password.get_secret_value())
    user_data["password_hash"] = password_plain
    del user_data["password"]

    new_user = await repo.create(user_data)
    return new_user
