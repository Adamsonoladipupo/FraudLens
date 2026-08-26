from typing import Any

from app.db.cognodb import cognodb


class DashboardRepository:

    def get_statistics(self) -> dict[str, Any]:

        query = """
        OPTIONAL MATCH (c:Customer)
        WITH count(c) AS customers

        OPTIONAL MATCH (a:Account)
        WITH customers, count(a) AS accounts

        OPTIONAL MATCH (t:Transaction)
        WITH customers, accounts, count(t) AS transactions

        OPTIONAL MATCH (highRisk:Transaction)
        WHERE highRisk.riskScore >= 70
        WITH
            customers,
            accounts,
            transactions,
            count(highRisk) AS high_risk_transactions

        OPTIONAL MATCH (d:Device)
        WITH
            customers,
            accounts,
            transactions,
            high_risk_transactions,
            count(d) AS devices

        OPTIONAL MATCH (ip:IPAddress)

        RETURN
            customers,
            accounts,
            transactions,
            high_risk_transactions,
            devices,
            count(ip) AS ip_addresses
        """

        result = cognodb.execute_query(query)

        if not result:
            return {}

        return result[0]