from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class TransactionResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    amount: float | None = None
    currency: str | None = None
    riskScore: float | None = None
    transactionType: str | None = None
    status: str | None = None
    timestamp: Any | None = None