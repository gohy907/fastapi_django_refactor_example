from domain.users.use_cases.create_user import CreateUserUseCase
from domain.users.use_cases.get_user_by_id import GetUserByIdUseCase


def create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()


def get_user_by_id_use_case() -> GetUserByIdUseCase:
    return GetUserByIdUseCase()
