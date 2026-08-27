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
    """
    Investigate a transaction and return its
    connected graph context and risk assessment.
    """

    result = service.investigate_transaction(
        transaction_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found",
        )

    return result


@router.get("/{transaction_id}/paths")
async def get_suspicious_paths(
    transaction_id: str,
):
    """
    Return suspicious graph paths associated
    with a transaction.
    """

    # First verify that the transaction exists.
    result = service.investigate_transaction(
        transaction_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found",
        )

    return service.get_suspicious_paths(
        transaction_id
    )
