from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from src.api.routes.users import router as users_router
from src.api.routes.categories import router as categories_router
from src.api.routes.posts import router as posts_router
from src.core.exceptions.domain_exceptions import (
    DatabaseError,
    UserAlreadyExistsException,
    UserUpdatingWithoutAuth,
    UserNotFoundByIdException,
    UserNotFoundByLoginException,
    CategoryAlreadyExistsException,
    CategoryNotFoundByIdException,
    CategoryNotFoundByTitleException,
)

from src.api.auth import router as auth_router

from src.core.config import settings

from http import HTTPStatus


def create_app() -> FastAPI:
    app = FastAPI(root_path=settings.API_ROOT)

    @app.exception_handler(DatabaseError)
    async def database_error_handler(request: Request, exc: DatabaseError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Database error occurred."},
        )

    @app.exception_handler(UserAlreadyExistsException)
    async def user_already_exists_handler(
        request: Request, exc: UserAlreadyExistsException
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": exc.message},
        )

    @app.exception_handler(UserUpdatingWithoutAuth)
    async def user_upgrading_without_auth(
        request: Request, exc: UserUpdatingWithoutAuth
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN, content={"message": exc.get_detail()}
        )

    @app.exception_handler(UserNotFoundByLoginException)
    async def user_not_found_by_login(
        request: Request, exc: UserNotFoundByLoginException
    ):
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={"message": exc.message},
        )

    @app.exception_handler(UserNotFoundByIdException)
    async def user_not_found_by_id(request: Request, exc: UserNotFoundByIdException):
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={"message": exc.message},
        )

    @app.exception_handler(CategoryAlreadyExistsException)
    async def category_already_exists_handler(
        request: Request, exc: CategoryAlreadyExistsException
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": exc.message},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        errors = []
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            message = error["msg"]
            errors.append(f"{field}: {message}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": errors},
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(users_router, prefix="/users", tags=["User APIs"])
    app.include_router(categories_router, prefix="/categories", tags=["Category APIs"])

    app.include_router(posts_router, prefix="/posts", tags=["Post APIs"])
    app.include_router(auth_router, tags=["Auth"])

    return app
