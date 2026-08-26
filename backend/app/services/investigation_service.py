from typing import Any

from app.repositories.investigation_repository import (
    InvestigationRepository,
)


class InvestigationService:

    def __init__(
            self,
            repository: InvestigationRepository,
    ) -> None:
        self.repository = repository

    def investigate_transaction(
            self,
            transaction_id: str,
    ) -> dict[str, Any] | None:

        result = self.repository.get_transaction_context(
            transaction_id
        )

        if result is None:
            return None

        transaction = result["t"]

        risk_score = transaction.get("riskScore", 0)

        if risk_score >= 70:
            risk_level = "HIGH"
        elif risk_score >= 40:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        connected_accounts = [
            account
            for account in result.get("connected_accounts", [])
            if account
               and account.get("id") != result["account"].get("id")
        ]

        connected_ip_accounts = [
            account
            for account in result.get(
                "connected_ip_accounts",
                [],
            )
            if account
               and account.get("id") != result["account"].get("id")
        ]

        indicators = []

        if connected_accounts:
            indicators.append({
                "code": "SHARED_DEVICE",
                "description": (
                    "Another account is using the same device."
                ),
                "score": 30,
            })

        if connected_ip_accounts:
            indicators.append({
                "code": "SHARED_IP",
                "description": (
                    "Another account is using the same IP address."
                ),
                "score": 20,
            })

        if risk_score >= 70:
            indicators.append({
                "code": "HIGH_TRANSACTION_RISK",
                "description": (
                    "Transaction has a high risk score."
                ),
                "score": risk_score,
            })

        return {
            "transaction": transaction,
            "account": result.get("account"),
            "customer": result.get("customer"),
            "merchant": result.get("merchant"),
            "devices": result.get("devices", []),
            "ip_addresses": result.get("ip_addresses", []),
            "connected_accounts": connected_accounts,
            "connected_ip_accounts": connected_ip_accounts,
            "risk_assessment": {
                "score": risk_score,
                "level": risk_level,
                "indicators": indicators,
            },
        }

    def get_suspicious_paths(
            self,
            transaction_id: str,
    ) -> list[dict[str, Any]]:
        return self.repository.get_suspicious_paths(
            transaction_id
        )