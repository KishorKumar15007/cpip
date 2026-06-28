from fastapi import FastAPI

from backend.api.routers.analytics import (
    router as analytics_router,
)

app = FastAPI(
    title="CP Intelligence Platform",
    version="1.0.0",
)

app.include_router(
    analytics_router,
)
