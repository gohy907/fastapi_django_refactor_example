from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from api.routes.users import router as users_router
from api.routes.categories import router as categories_router
from core.exceptions.exc import DatabaseError, UserAlreadyExistsError, CategoryAlreadyExistsError, UserDoesNotExist
from api.auth import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1")

    @app.exception_handler(DatabaseError)
    async def database_error_handler(request: Request, exc: DatabaseError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Database error occurred."},
        )

    @app.exception_handler(UserAlreadyExistsError)
    async def user_already_exists_handler(
        request: Request, exc: UserAlreadyExistsError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": exc.message},
        )

    @app.exception_handler(UserDoesNotExist)
    async def user_does_not_exist(
        request: Request, exc: UserDoesNotExist
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": exc.message},
        )

    @app.exception_handler(CategoryAlreadyExistsError)
    async def category_already_exists_handler(
        request: Request, exc: CategoryAlreadyExistsError
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
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
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
    app.include_router(categories_router,
                       prefix="/categories", tags=["Category APIs"])
    app.include_router(auth_router, tags=["Auth"])

    return app
