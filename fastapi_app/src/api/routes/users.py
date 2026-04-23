import uuid

from domain.users.use_cases.create_user import CreateUserUseCase
from domain.users.use_cases.get_user_by_id import GetUserByIdUseCase
from schemas.users import CreateUser, UserResponse
from fastapi import APIRouter, Depends,  status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import database

from api.routes.depends import create_user_use_case, get_user_by_id_use_case, get_get_user_by_login_use_case
from repositories.users import UserRepository


from domain.users.use_cases.get_user_by_login import GetUserByLoginUseCase
from core.exceptions.domain_exceptions import UserNotFoundByLoginException, UserLoginIsNotUniqueException
from services.auth import AuthService

router = APIRouter()


async def get_db():
    async with database.session() as session:
        yield session


# @router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
# async def get_user_by_id(
#     id: uuid.UUID,
#     session: AsyncSession = Depends(get_db),
#     use_case: GetUserByIdUseCase = Depends(get_user_by_id_use_case)
# ) -> UserResponse:
#     user = await use_case.execute(session=session, id=id)
#     return user


# @router.post(
#     "/register", response_model=User, status_code=status.HTTP_201_CREATED
# )
# async def register_user(user_in: CreateUser, db: AsyncSession = Depends(get_db)):
#     repo = UserRepository(db)
#
#     user_data = user_in.model_dump()
#     password_plain = str(user_in.password.get_secret_value())
#     user_data["password_hash"] = password_plain
#     del user_data["password"]
#
#     new_user = await repo.create(user_data)
#     return new_user


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
    user: CreateUser,
    use_case: CreateUserUseCase = Depends(create_user_use_case),
    session: AsyncSession = Depends(get_db)
) -> UserResponse:
    try:

        user = await use_case.execute(user_in=user, session=session)
        return user
    except UserLoginIsNotUniqueException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail())
