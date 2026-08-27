from typing import Any

from app.db.cognodb import cognodb


class InvestigationRepository:

    def get_transaction_context(
        self,
        transaction_id: str,
    ) -> dict[str, Any] | None:
        """
        Retrieve the transaction and the connected graph
        relevant to a fraud investigation.
        """

        query = """
        MATCH (t:Transaction {id: $transaction_id})

        OPTIONAL MATCH (account:Account)-[:MAKES]->(t)

        OPTIONAL MATCH (customer:Customer)-[:OWNS]->(account)

        OPTIONAL MATCH (t)-[:TO]->(merchant:Merchant)

        OPTIONAL MATCH (account)-[:USES_DEVICE]->(device:Device)

        OPTIONAL MATCH (otherAccount:Account)-[:USES_DEVICE]->(device)

        OPTIONAL MATCH (account)-[:USES_IP]->(ip:IPAddress)

        OPTIONAL MATCH (otherIpAccount:Account)-[:USES_IP]->(ip)

        OPTIONAL MATCH (account)-[:MAKES]->(accountTransaction:Transaction)

        OPTIONAL MATCH (otherAccount)-[:MAKES]->(deviceTransaction:Transaction)

        OPTIONAL MATCH (otherIpAccount)-[:MAKES]->(ipTransaction:Transaction)

        RETURN
            t,
            account,
            customer,
            merchant,

            collect(DISTINCT device) AS devices,

            collect(DISTINCT ip) AS ip_addresses,

            collect(DISTINCT otherAccount) AS connected_accounts,

            collect(DISTINCT otherIpAccount) AS connected_ip_accounts,

            collect(DISTINCT accountTransaction) AS account_transactions,

            collect(DISTINCT deviceTransaction) AS device_transactions,

            collect(DISTINCT ipTransaction) AS ip_transactions
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

    def get_suspicious_paths(
        self,
        transaction_id: str,
    ) -> list[dict[str, Any]]:
        """
        Find potentially suspicious graph paths connected
        to a transaction.

        A suspicious path exists when another account is
        connected through a shared device or IP address.
        """

        query = """
        MATCH (t:Transaction {id: $transaction_id})

        OPTIONAL MATCH (account:Account)-[:MAKES]->(t)

        OPTIONAL MATCH path =
            (account)-[:USES_DEVICE|USES_IP]->(node)<-
            [:USES_DEVICE|USES_IP]-(otherAccount:Account)

        WHERE otherAccount.id <> account.id

        RETURN DISTINCT
            otherAccount.id AS connected_account_id,
            labels(node)[0] AS connection_type,
            node.id AS connection_id
        """

        records = cognodb.execute_query(
            query,
            {
                "transaction_id": transaction_id,
            },
        )

        return records or []
