from domain.users.use_cases.create_user import CreateUserUseCase
from domain.users.use_cases.get_user_by_id import GetUserByIdUseCase
from domain.categories.use_cases.create_category import CreateCategoryUseCase
from domain.categories.use_cases.get_category import GetCategoryByIdUseCase


def create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()


def get_user_by_id_use_case() -> GetUserByIdUseCase:
    return GetUserByIdUseCase()


def create_category_use_case() -> CreateCategoryUseCase:
    return CreateCategoryUseCase()


def get_category_by_id_use_case() -> GetCategoryByIdUseCase:
    return GetCategoryByIdUseCase()
