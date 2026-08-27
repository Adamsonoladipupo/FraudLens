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

    def get_transactions(
            self,
            limit: int = 50,
            risk_level: str | None = None,
            status: str | None = None,
            transaction_type: str | None = None,
            transaction_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Retrieve transactions with optional filters.
        """

        conditions = []
        parameters: dict[str, Any] = {
            "limit": limit,
        }

        if transaction_id:
            conditions.append("t.id = $transaction_id")
            parameters["transaction_id"] = transaction_id

        if status:
            conditions.append("t.status = $status")
            parameters["status"] = status

        if transaction_type:
            conditions.append(
                "t.transactionType = $transaction_type"
            )
            parameters["transaction_type"] = transaction_type

        if risk_level == "LOW":
            conditions.append("t.riskScore < 40")

        elif risk_level == "MEDIUM":
            conditions.append(
                "t.riskScore >= 40 AND t.riskScore < 70"
            )

        elif risk_level == "HIGH":
            conditions.append("t.riskScore >= 70")

        where_clause = ""

        if conditions:
            where_clause = (
                    "WHERE " + " AND ".join(conditions)
            )

        query = f"""
        MATCH (t:Transaction)

        {where_clause}

        RETURN
            t.id AS id,
            t.amount AS amount,
            t.currency AS currency,
            t.riskScore AS riskScore,
            t.transactionType AS transactionType,
            t.status AS status,
            t.timestamp AS timestamp

        ORDER BY t.timestamp DESC

        LIMIT $limit
        """

        records = cognodb.execute_query(
            query,
            parameters,
        )

        return records or []

    def get_recent_transactions(
            self,
            limit: int = 50,
    ) -> list[dict[str, Any]]:
        """
        Retrieve the most recent transactions.

        Kept for backwards compatibility.
        """

        return self.get_transactions(
            limit=limit,
        )