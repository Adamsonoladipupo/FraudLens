from datetime import datetime

from pydantic import BaseModel


class IPAddress(BaseModel):
    id: str
    address: str
    country: str
    first_seen_at: datetime
    last_seen_at: datetime