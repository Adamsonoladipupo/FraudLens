from app.db.cognodb import cognodb


def main():
    cognodb.connect()

    try:
        cognodb.verify_connection()

        query = """
        MATCH (a:Account)-[r]->(b)
        RETURN
            a.id AS source,
            type(r) AS relationship,
            labels(b) AS target_type,
            b.id AS target
        LIMIT 50
        """

        results = cognodb.execute_query(query)

        print("\nGraph relationships:")
        for result in results:
            print(result)

    finally:
        cognodb.close()


if __name__ == "__main__":
    main()