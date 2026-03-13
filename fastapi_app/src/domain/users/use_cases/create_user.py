from repositories.users import UserRepository
from schemas.users import UserResponse, UserCreate
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession


class CreateUserUseCase:

    def __init__(self):
        pass

    async def execute(self, session: AsyncSession, user_in: UserCreate) -> UserResponse:
        repo = UserRepository(session)

        user_data = user_in.model_dump()
        user_data["password_hash"] = user_in.password.get_secret_value()
        del user_data["password"]
        user = await repo.create(user_data)
        await session.commit()

        return UserResponse.model_validate(user)
