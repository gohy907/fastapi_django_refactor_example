from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routes.users import router as user_router
from api.routes.categories import router as category_router


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1")
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(category_router, prefix="/categories/",
                       tags=["Category APIs"])
    app.include_router(user_router, prefix="/users/", tags=["User APIs"])

    return app
