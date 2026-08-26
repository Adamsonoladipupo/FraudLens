from pydantic import BaseModel, Field

from app.schemas.account import Account
from app.schemas.customer import Customer
from app.schemas.device import Device
from app.schemas.ip_address import IPAddress
from app.schemas.merchant import Merchant
from app.schemas.risk import RiskAssessment
from app.schemas.transaction import Transaction


class TransactionInvestigation(BaseModel):
    transaction: Transaction
    customer: Customer | None = None
    account: Account | None = None
    merchant: Merchant | None = None
    devices: list[Device] = Field(default_factory=list)
    ip_addresses: list[IPAddress] = Field(default_factory=list)
    risk_assessment: RiskAssessment