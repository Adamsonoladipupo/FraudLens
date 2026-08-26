from enum import Enum

from pydantic import BaseModel


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class RiskIndicator(BaseModel):
    code: str
    description: str
    score: int


class RiskAssessment(BaseModel):
    score: int
    level: RiskLevel
    indicators: list[RiskIndicator]