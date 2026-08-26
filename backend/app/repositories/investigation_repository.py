from typing import Any

from app.db.cognodb import cognodb


class InvestigationRepository:

    def get_transaction_context(
        self,
        transaction_id: str,
    ) -> dict[str, Any] | None:
        """
        Retrieve the graph context surrounding a transaction.
        """

        query = """
        MATCH (t:Transaction {id: $transaction_id})

        OPTIONAL MATCH (account:Account)-[:MAKES]->(t)
        OPTIONAL MATCH (customer:Customer)-[:OWNS]->(account)
        OPTIONAL MATCH (t)-[:TO]->(merchant:Merchant)
        OPTIONAL MATCH (account)-[:USES_DEVICE]->(device:Device)
        OPTIONAL MATCH (account)-[:USES_IP]->(ip:IPAddress)

        RETURN
            t,
            account,
            customer,
            merchant,
            collect(DISTINCT device) AS devices,
            collect(DISTINCT ip) AS ip_addresses
        """

        records = cognodb.execute_query(
            query,
            {
                "transaction_id": transaction_id,
            },
        )

        if not records:
            return None

        return records[0]