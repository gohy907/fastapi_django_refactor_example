from src.repositories.posts import PostRepository

from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.posts import PostCreate, PostResponse
from src.core.db import database


import logging
logger = logging.getLogger(__name__)


class CreatePostUseCase:
    def __init__(self):
        self._database = database

    async def execute(self, session: AsyncSession, post_create: PostCreate) -> PostResponse:
        repo = PostRepository()

        post = await repo.create(session=session, post_create=post_create)

        await session.commit()

        logger.info(f"Post {post.title} has been created")
        return PostResponse.model_validate(post)
        # except PostAlreadyExistsException:
        #     logger.info(
        #         f"Post {post_create.title} already exists, aborting creation")
        #     raise UserLoginIsNotUniqueException(login=user_in.login)
