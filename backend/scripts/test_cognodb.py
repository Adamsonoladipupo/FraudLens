from app.db.cognodb import cognodb


def main() -> None:
    cognodb.connect()

    try:
        cognodb.verify_connection()

        result = cognodb.execute_query(
            """
            RETURN 'FraudLens' AS application
            """
        )

        print(result)

    finally:
        cognodb.close()


if __name__ == "__main__":
    main()
