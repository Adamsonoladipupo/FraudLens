from enum import Enum


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class TransactionStatus(str, Enum):
    COMPLETED = "COMPLETED"

class TransactionType(str, Enum):
    PURCHASE = "PURCHASE"
    TRANSFER = "TRANSFER"
    WITHDRAWAL = "WITHDRAWAL"
    PAYMENT = "PAYMENT"