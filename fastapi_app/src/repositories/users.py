# repositories/users.py
import uuid
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from repositories.base import BaseRepository
from core.exceptions import UserAlreadyExistsError

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def create(self, data: dict) -> User:
        try:
            return await super().create(data)
        except IntegrityError:
            raise UserAlreadyExistsError()

    async def does_user_exist_by_login(self, login: str) -> bool:
        query = select(User).where(User.login == login)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None
