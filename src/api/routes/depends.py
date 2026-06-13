from src.domain.users.use_cases.create_user import CreateUserUseCase
from src.domain.users.use_cases.get_user_by_id import GetUserByIdUseCase
from src.domain.categories.use_cases.create_category import CreateCategoryUseCase
from src.domain.categories.use_cases.get_category import (
    GetCategoryByIdUseCase,
    GetCategoryByTitleUseCase,
)
from src.domain.users.use_cases.get_user_by_login import GetUserByLoginUseCase
from src.domain.auth.use_cases.authenticate_user import AuthenticateUserUseCase
from src.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase
from src.domain.users.use_cases.update_user import UpdateUserUseCase
from src.domain.posts.use_cases.create_post import CreatePostUseCase


def update_user_use_case() -> UpdateUserUseCase:
    return UpdateUserUseCase(get_user_use_case=get_user_by_id_use_case())


def create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()


def get_get_user_by_login_use_case() -> GetUserByLoginUseCase:
    return GetUserByLoginUseCase()


def get_user_by_id_use_case() -> GetUserByIdUseCase:
    return GetUserByIdUseCase()


def create_category_use_case() -> CreateCategoryUseCase:
    return CreateCategoryUseCase()


def get_category_by_id_use_case() -> GetCategoryByIdUseCase:
    return GetCategoryByIdUseCase()


def get_category_by_title_use_case() -> GetCategoryByTitleUseCase:
    return GetCategoryByTitleUseCase()


def authenticate_user_use_case() -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase()


def create_access_token_use_case() -> CreateAccessTokenUseCase:
    return CreateAccessTokenUseCase()


def create_post_use_case() -> CreatePostUseCase:
    return CreatePostUseCase()
