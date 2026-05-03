from src.core.db import database
from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas.auth import Token
from src.domain.auth.use_cases.authenticate_user import AuthenticateUserUseCase
from src.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase
from src.core.exceptions.domain_exceptions import WrongPasswordException, UserNotFoundByLoginException
from src.api.routes.depends import create_access_token_use_case, authenticate_user_use_case
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db():
    async with database.session() as session:
        yield session

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_use_case: Annotated[AuthenticateUserUseCase, Depends(authenticate_user_use_case)],
    create_token_use_case: CreateAccessTokenUseCase = Depends(
        create_access_token_use_case),
    session: AsyncSession = Depends(get_db)
) -> Token:

    try:
        user = await auth_use_case.execute(login=form_data.username, password=form_data.password, session=session)
    except WrongPasswordException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.get_detail(),
            headers={"WWW-Authenticate": "Bearer"},
        )

    except UserNotFoundByLoginException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())
    access_token = await create_token_use_case.execute(login=user.login)
    return Token(access_token=access_token, token_type="bearer")
