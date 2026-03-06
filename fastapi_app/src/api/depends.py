from domain.user.use_cases.get_user_by_login import GetUserByLoginUseCase


def get_get_user_by_login_use_case() -> GetUserByLoginUseCase:
    return GetUserByLoginUseCase()
