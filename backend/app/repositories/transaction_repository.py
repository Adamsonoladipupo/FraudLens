from typing import Any

from app.db.cognodb import cognodb


class TransactionRepository:

    def find_by_id(
        self,
        transaction_id: str,
    ) -> dict[str, Any] | None:
        """
        Find a transaction by its ID.
        """

        query = """
        MATCH (t:Transaction {id: $transaction_id})
        RETURN t
        LIMIT 1
        """

        records = cognodb.execute_query(
            query,
            {
                "transaction_id": transaction_id,
            },
        )

        if not records:
            return None

        return records[0]["t"]