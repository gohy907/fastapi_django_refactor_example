from src.repositories.posts import PostRepository
from src.repositories.users import UserRepository
from src.repositories.categories import CategoryRepository


from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.posts import PostCreate, PostResponse
from src.core.db import database

from src.schemas.users import UserResponse

from src.core.exceptions.database_exceptions import EntityNotFoundException
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByIdException,
    CategoryNotFoundByIdException,
    UserDoingForbiddenActions,
)


import logging

logger = logging.getLogger(__name__)


class CreatePostUseCase:
    def __init__(self):
        self._database = database

    async def execute(
        self, session: AsyncSession, current_user: UserResponse, post_create: PostCreate
    ) -> PostResponse:

        user_repo = UserRepository(session)
        try:
            await user_repo.get_by_id(id=post_create.author_id)
        except EntityNotFoundException:
            raise UserNotFoundByIdException(id=post_create.author_id)

        if current_user.id != post_create.author_id:
            raise UserDoingForbiddenActions(id=current_user.id)

        category_repo = CategoryRepository(session)

        try:
            await category_repo.get_by_id(id=post_create.category_id)
        except EntityNotFoundException:
            raise CategoryNotFoundByIdException(id=post_create.category_id)

        post_repo = PostRepository(session)

        post = await post_repo.create(post_create=post_create)

        await session.flush()

        logger.info(f"Post {post.title} has been created")
        return PostResponse.model_validate(post)
