from datetime import datetime

from pydantic import BaseModel, EmailStr


class Customer(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    phone: str
    status: str
    created_at: datetime