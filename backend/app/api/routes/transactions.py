from fastapi import APIRouter, HTTPException, Query

from app.repositories.transaction_repository import (
    TransactionRepository,
)
from app.services.transaction_service import (
    TransactionService,
)
from app.schemas.transaction import TransactionResponse
from app.schemas.enums import RiskLevel, TransactionStatus, TransactionType


router = APIRouter(
    prefix="/api/transactions",
    tags=["Transactions"],
)


repository = TransactionRepository()
service = TransactionService(repository)


@router.get(
    "",
    response_model=list[TransactionResponse],
    summary="Get Transactions",
    description=(
            "Return transactions with optional filters. "
            "Transactions are retrieved from CognoDB using "
            "parameterized openCypher queries."
    ),
)
async def get_transactions(
        limit: int = Query(
            default=50,
            ge=1,
            le=100,
            description="Maximum number of transactions to return.",
        ),
        risk_level: RiskLevel | None = Query(
            default=None,
            description="Filter by risk level.",
        ),
        status: TransactionStatus | None = Query(
            default=None,
            description="Filter by transaction status.",
        ),
        transaction_type: TransactionType | None = Query(
            default=None,
            description="Filter by transaction type.",
        ),
        transaction_id: str | None = Query(
            default=None,
            description="Filter by transaction ID.",
        ),
):
    """
    Return transactions with optional filters.
    """

    try:
        return service.get_transactions(
            limit=limit,
            risk_level=risk_level,
            status=status,
            transaction_type=transaction_type,
            transaction_id=transaction_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )