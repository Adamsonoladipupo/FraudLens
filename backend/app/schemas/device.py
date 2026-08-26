from datetime import datetime

from pydantic import BaseModel


class Device(BaseModel):
    id: str
    device_fingerprint: str
    device_type: str
    first_seen_at: datetime
    last_seen_at: datetime