from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.cognodb import cognodb

from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.investigations import (
    router as investigations_router,
)
from app.api.routes.transactions import (
    router as transactions_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown.
    """

    # Startup
    try:
        cognodb.connect()
        cognodb.verify_connection()
        print("Successfully connected to CognoDB Cloud.")
    except Exception as exc:
        print(f"Warning: Unable to connect to CognoDB Cloud: {exc}")

    yield

    # Shutdown
    cognodb.close()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Graph-powered retail banking fraud investigation "
        "and risk exploration API."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router)
app.include_router(investigations_router)
app.include_router(transactions_router)


@app.get("/")
async def root():
    return {
        "application": settings.app_name,
        "message": "FraudLens API is running",
        "version": settings.app_version,
    }


@app.get("/health")
async def health_check():
    database_status = "connected"

    try:
        cognodb.verify_connection()
    except Exception:
        database_status = "unavailable"

    return {
        "status": "ok",
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "database": database_status,
    }