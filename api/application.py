from api.handlers import router
from fastapi import FastAPI
from fastapi.responses import UJSONResponse


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    :return: FastAPI
    """

    app = FastAPI(
        title="Database practise",
        description="Small db server",
        version="0.0.1",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        default_response_class=UJSONResponse,
    )

    app.include_router(
        router=router,
        prefix="/api",
    )

    return app
