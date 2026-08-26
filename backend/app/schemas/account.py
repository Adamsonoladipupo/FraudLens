from datetime import datetime

from pydantic import BaseModel


class Account(BaseModel):
    id: str
    account_number: str
    account_type: str
    status: str
    opened_at: datetime
    risk_level: str