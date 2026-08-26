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

        RETURN
            t,
            account,
            customer,
            merchant,
            collect(DISTINCT device) AS devices,
            collect(DISTINCT otherAccount) AS connected_accounts,
            collect(DISTINCT ip) AS ip_addresses,
            collect(DISTINCT otherIpAccount) AS connected_ip_accounts
        """

        records = cognodb.execute_query(
            query,
            {"transaction_id": transaction_id},
        )

        if not records:
            return None

        return records[0]

    def get_suspicious_paths(
            self,
            transaction_id: str,
    ) -> list[dict[str, Any]]:
        """
        Find multi-hop relationships around a transaction
        that may indicate coordinated fraud.
        """

        query = """
        MATCH (t:Transaction {id: $transaction_id})
        MATCH (account:Account)-[:MAKES]->(t)

        MATCH path =
            (account)-[:USES_DEVICE|USES_IP]->(shared)
            <-[:USES_DEVICE|USES_IP]-(otherAccount:Account)
            -[:MAKES]->(otherTransaction:Transaction)

        WHERE otherAccount.id <> account.id
          AND otherTransaction.id <> t.id

        RETURN
            labels(shared)[0] AS shared_entity_type,
            shared.id AS shared_entity_id,
            otherAccount.id AS connected_account_id,
            otherTransaction.id AS connected_transaction_id,
            length(path) AS hops
        ORDER BY hops ASC
        """

        return cognodb.execute_query(
            query,
            {"transaction_id": transaction_id},
        )