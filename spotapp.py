from fastapi import FastAPI
from api.constants import API_TITLE

from api.settings import configure_logger
from api.routes import spotapp_router


def spotapp_api() -> FastAPI:
    configure_logger(API_TITLE)
    app = FastAPI(
        title=API_TITLE,
        description="not forgot to fill",
        docs_url="/docs",
    )
    app.include_router(spotapp_router)
    return app


app = application = api = spotapp_api()


@app.get("/health")
async def health_check():
    return {"message": "Just a health check"}
