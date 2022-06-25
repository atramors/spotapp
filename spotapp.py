from fastapi import FastAPI, HTTPException
from api.constants import API_TITLE
from api.middleware import http_exception_handler

from api.settings import configure_logger
from api.routes import spotapp_user_router, spotapp_spot_router, spotapp_comment_router
from api.authentication import spotapp_auth_router


def spotapp_api() -> FastAPI:
    configure_logger(API_TITLE)
    app = FastAPI(
        title=API_TITLE,
        description="not forgot to fill",
        docs_url="/docs",
    )
    app.add_exception_handler(HTTPException, http_exception_handler)

    app.include_router(spotapp_auth_router)
    app.include_router(spotapp_user_router)
    app.include_router(spotapp_spot_router)
    app.include_router(spotapp_comment_router)

    return app


app = application = api = spotapp_api()


@app.get("/health")
async def health_check():
    return {"message": "Just a health check"}
