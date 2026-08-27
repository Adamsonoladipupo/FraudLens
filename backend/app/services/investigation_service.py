from typing import Any

from app.repositories.investigation_repository import (
    InvestigationRepository,
)
from app.utils.serialization import (
    serialize_neo4j_value,
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

        account = result.get("account")

        connected_accounts = [
            account
            for account in result.get(
                "connected_accounts",
                [],
            )
            if account
               and (
                       not result.get("account")
                       or account.get("id")
                       != result["account"].get("id")
               )
        ]

        connected_ip_accounts = [
            account
            for account in result.get(
                "connected_ip_accounts",
                [],
            )
            if account
               and (
                       not result.get("account")
                       or account.get("id")
                       != result["account"].get("id")
               )
        ]

        related_transactions = []

        related_transactions.extend(
            result.get("account_transactions", [])
        )

        related_transactions.extend(
            result.get("device_transactions", [])
        )

        related_transactions.extend(
            result.get("ip_transactions", [])
        )

        # Remove duplicates while preserving transaction data.
        unique_transactions = {}

        for related_transaction in related_transactions:
            if not related_transaction:
                continue

            transaction_id_value = related_transaction.get("id")

            if transaction_id_value:
                unique_transactions[
                    transaction_id_value
                ] = related_transaction

        related_transactions = list(
            unique_transactions.values()
        )

        indicators = []

        if connected_accounts:
            indicators.append({
                "code": "SHARED_DEVICE",
                "description": (
                    "Another account is connected "
                    "through a shared device."
                ),
                "score": 30,
            })

        if connected_ip_accounts:
            indicators.append({
                "code": "SHARED_IP",
                "description": (
                    "Another account is connected "
                    "through a shared IP address."
                ),
                "score": 20,
            })

        if len(connected_accounts) >= 2:
            indicators.append({
                "code": "MULTIPLE_CONNECTED_ACCOUNTS",
                "description": (
                    "Multiple accounts are connected "
                    "to the same device."
                ),
                "score": 25,
            })

        if risk_score >= 70:
            indicators.append({
                "code": "HIGH_TRANSACTION_RISK",
                "description": (
                    "Transaction has a high risk score."
                ),
                "score": risk_score,
            })

        response = {
            "transaction": transaction,
            "account": account,
            "customer": result.get("customer"),
            "merchant": result.get("merchant"),
            "devices": result.get(
                "devices",
                [],
            ),
            "ip_addresses": result.get(
                "ip_addresses",
                [],
            ),
            "connected_accounts": connected_accounts,
            "connected_ip_accounts": connected_ip_accounts,
            "related_transactions": related_transactions,
            "risk_assessment": {
                "score": risk_score,
                "level": risk_level,
                "indicators": indicators,
            },
        }

        return serialize_neo4j_value(response)

    def get_suspicious_paths(
            self,
            transaction_id: str,
    ) -> list[dict[str, Any]]:
        """
        Return suspicious connections associated
        with a transaction.
        """

        paths = self.repository.get_suspicious_paths(
            transaction_id
        )

        return [
            serialize_neo4j_value(path)
            for path in paths
        ]