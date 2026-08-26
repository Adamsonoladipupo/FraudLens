from pydantic import BaseModel


class Merchant(BaseModel):
    id: str
    name: str
    category: str
    country: str
    status: str