from typing import Any


def serialize_neo4j_value(value: Any) -> Any:
    """
    Convert Neo4j values into JSON-friendly Python values.

    In particular, Neo4j temporal values such as DateTime
    are converted into ISO-8601 strings.
    """

    if value is None:
        return None

    if isinstance(value, dict):
        return {
            key: serialize_neo4j_value(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            serialize_neo4j_value(item)
            for item in value
        ]

    if isinstance(value, tuple):
        return [
            serialize_neo4j_value(item)
            for item in value
        ]

    # Neo4j temporal values expose iso_format().
    if hasattr(value, "iso_format"):
        return value.iso_format()

    # Python datetime/date/time objects.
    if hasattr(value, "isoformat"):
        return value.isoformat()

    return value
