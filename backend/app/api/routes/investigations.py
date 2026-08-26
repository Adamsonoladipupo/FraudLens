from fastapi import APIRouter, HTTPException

from app.repositories.investigation_repository import (
    InvestigationRepository,
)
from app.services.investigation_service import (
    InvestigationService,
)


router = APIRouter(
    prefix="/api/investigations",
    tags=["Investigations"],
)


repository = InvestigationRepository()
service = InvestigationService(repository)


@router.get("/{transaction_id}")
async def investigate_transaction(
        transaction_id: str,
):
    result = service.investigate_transaction(
        transaction_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found",
        )

    suspicious_paths = service.get_suspicious_paths(
        transaction_id
    )

    result["suspicious_paths"] = suspicious_paths

    return result