from typing import Any

from app.db.cognodb import cognodb


class AccountRepository:

    def find_by_id(
        self,
        account_id: str,
    ) -> dict[str, Any] | None:
        """
        Find an account by its ID.
        """

        query = """
        MATCH (a:Account {id: $account_id})
        RETURN a
        LIMIT 1
        """

        records = cognodb.execute_query(
            query,
            {
                "account_id": account_id,
            },
        )

        if not records:
            return None

        return records[0]["a"]

    def find_accounts_sharing_device(
        self,
        account_id: str,
    ) -> list[dict[str, Any]]:
        """
        Find other accounts connected to the same device.
        """

        query = """
        MATCH (account:Account {id: $account_id})
              -[:USES_DEVICE]->(device:Device)
              <-[:USES_DEVICE]-(other:Account)

        WHERE other.id <> $account_id

        RETURN DISTINCT other
        """

        records = cognodb.execute_query(
            query,
            {
                "account_id": account_id,
            },
        )

        return [record["other"] for record in records]

    def find_accounts_sharing_ip(
        self,
        account_id: str,
    ) -> list[dict[str, Any]]:
        """
        Find other accounts connected to the same IP address.
        """

        query = """
        MATCH (account:Account {id: $account_id})
              -[:USES_IP]->(ip:IPAddress)
              <-[:USES_IP]-(other:Account)

        WHERE other.id <> $account_id

        RETURN DISTINCT other
        """

        records = cognodb.execute_query(
            query,
            {
                "account_id": account_id,
            },
        )

        return [record["other"] for record in records]