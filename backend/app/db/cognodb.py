from typing import Any

from neo4j import Driver, GraphDatabase

from app.core.config import settings


class CognoDB:
    """
    Manages the connection to CognoDB Cloud.
    """

    def __init__(self) -> None:
        self._driver: Driver | None = None

    def connect(self) -> None:
        """Create the CognoDB database driver."""

        if not settings.cognodb_uri:
            raise ValueError("COGNODB_URI is not configured")

        if not settings.cognodb_username:
            raise ValueError("COGNODB_USERNAME is not configured")

        if not settings.cognodb_password:
            raise ValueError("COGNODB_PASSWORD is not configured")

        self._driver = GraphDatabase.driver(
            settings.cognodb_uri,
            auth=(
                settings.cognodb_username,
                settings.cognodb_password,
            ),
        )

    def verify_connection(self) -> bool:
        """Verify that CognoDB is reachable."""

        if self._driver is None:
            raise RuntimeError(
                "CognoDB driver has not been initialized"
            )

        self._driver.verify_connectivity()
        return True

    def execute_query(
        self,
        query: str,
        parameters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Execute a parameterized Cypher query.

        Returns query records as dictionaries.
        """

        if self._driver is None:
            raise RuntimeError(
                "CognoDB driver has not been initialized"
            )

        with self._driver.session() as session:
            result = session.run(
                query,
                parameters or {},
            )

            return [record.data() for record in result]

    def close(self) -> None:
        """Close the database connection."""

        if self._driver is not None:
            self._driver.close()
            self._driver = None

    @property
    def driver(self) -> Driver:
        """Return the active database driver."""

        if self._driver is None:
            raise RuntimeError(
                "CognoDB driver has not been initialized"
            )

        return self._driver


cognodb = CognoDB()