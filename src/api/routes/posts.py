import uuid

from src.schemas.posts import PostCreate, PostResponse
from fastapi import APIRouter, Depends,  status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import database

from src.api.routes.depends import create_post_use_case

from src.domain.posts.use_cases.create_post import CreatePostUseCase


router = APIRouter()


async def get_db():
    async with database.session() as session:
        yield session

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(
    post: PostCreate,
    use_case: CreatePostUseCase = Depends(create_post_use_case),
    session: AsyncSession = Depends(get_db)
) -> PostResponse:
    post = await use_case.execute(post_create=post, session=session)
    return post
