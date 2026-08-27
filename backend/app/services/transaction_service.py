from typing import Any

from app.repositories.transaction_repository import (
    TransactionRepository,
)
from app.utils.serialization import (
    serialize_neo4j_value,
)


class TransactionService:

    def __init__(
            self,
            repository: TransactionRepository,
    ) -> None:
        self.repository = repository

    def get_recent_transactions(
            self,
            limit: int = 50,
    ) -> list[dict[str, Any]]:
        """
        Retrieve recent transactions.
        """

        if limit < 1:
            limit = 1

        if limit > 100:
            limit = 100

        transactions = self.repository.get_recent_transactions(
            limit
        )

        return [
            serialize_neo4j_value(transaction)
            for transaction in transactions
        ]

    def find_transaction(
            self,
            transaction_id: str,
    ) -> dict[str, Any] | None:
        """
        Find a transaction by ID.
        """

        transaction = self.repository.find_by_id(
            transaction_id
        )

        if transaction is None:
            return None

        return serialize_neo4j_value(transaction)