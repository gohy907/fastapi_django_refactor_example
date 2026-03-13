import uuid

from repositories.users import UserRepository
from schemas.users import UserResponse
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession


class GetUserByIdUseCase:

    def __init__(self):
        pass

    async def execute(self, session: AsyncSession, id: uuid.UUID) -> UserResponse:
        repo = UserRepository(session)

        user = await repo.get(id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return UserResponse.model_validate(user)
