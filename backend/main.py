from fastapi import FastAPI

from backend.api.routers.analytics import (
    router as analytics_router,
)
from backend.api.routers.sync import (
    router as sync_router,
)
from backend.api.routers.auth import router as auth_router
from backend.api.routers.problems import router as problems_router
from backend.api.routers.submissions import router as submissions_router

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

app.include_router(auth_router)

app.include_router(problems_router)

app.include_router(submissions_router)
