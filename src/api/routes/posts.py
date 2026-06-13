from src.schemas.users import UserResponse
from src.schemas.posts import PostCreate, PostResponse
from src.services.auth import AuthService
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db

from src.api.routes.depends import create_post_use_case

from src.domain.posts.use_cases.create_post import CreatePostUseCase

from src.core.exceptions.domain_exceptions import (
    UserNotFoundByIdException,
    CategoryNotFoundByIdException,
    UserDoingForbiddenActions,
)


router = APIRouter()


@router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=PostResponse
)
async def create_post(
    post: PostCreate,
    use_case: CreatePostUseCase = Depends(create_post_use_case),
    current_user: UserResponse = Depends(AuthService.get_current_user),
    session: AsyncSession = Depends(get_db),
) -> PostResponse:
    try:
        post = await use_case.execute(
            post_create=post, current_user=current_user, session=session
        )
    except UserDoingForbiddenActions as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.get_detail()
        )
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.get_detail()
        )

    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.get_detail()
        )

    return post
