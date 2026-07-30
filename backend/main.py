from fastapi import FastAPI

from backend.api.routers.analytics import (
    router as analytics_router,
)
from backend.api.routers.sync import (
    router as sync_router,
)

app = FastAPI(
    title="CP Intelligence Platform",
    version="1.0.0",
)

app.include_router(
    analytics_router,
)

app.include_router(
    sync_router,
)
