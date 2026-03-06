from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import User as UserSchema


class GetUserByLoginUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, login: str) -> UserSchema:
        with self._database.session() as session:
            user = self._repo.get(session=session, login=login)

        return UserSchema.model_validate(obj=user)
