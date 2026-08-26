from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.db.cognodb import cognodb


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