from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Transaction(BaseModel):
    id: str
    amount: Decimal
    currency: str
    timestamp: datetime
    transaction_type: str
    status: str
    risk_score: int