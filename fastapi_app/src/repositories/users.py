import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    # async def get_by_l(self, login: str) -> Optional[User]:
    #     result = await self.get(login)
    #     return result.scalar_one_or_none()
        # query = select(User).where(User.login == login)
        # result = await self.session.execute(query)
        # return result.scalar_one_or_none()

    async def does_user_exist_by_login(self, login: str) -> bool:
        query = select(User).where(
            User.login == login)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def does_user_exist_by_id(self, id: uuid.UUID) -> bool:
        query = select(User).where(
            User.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None
