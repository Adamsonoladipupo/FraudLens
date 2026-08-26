from fastapi import APIRouter

from app.repositories.dashboard_repository import (
    DashboardRepository,
)
from app.services.dashboard_service import DashboardService


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)


repository = DashboardRepository()
service = DashboardService(repository)


@router.get("")
async def get_dashboard():
    return service.get_statistics()