from app.db.cognodb import cognodb


def main():
    cognodb.connect()

    try:
        result = cognodb.execute_query(
            """
            MATCH (a:Account)-[:USES_DEVICE]->(d:Device)
                  <-[:USES_DEVICE]-(other:Account)

            WHERE a.id <> other.id

            RETURN
                a.id AS account,
                d.id AS shared_device,
                other.id AS connected_account

            LIMIT 10
            """
        )

        for record in result:
            print(record)

    finally:
        cognodb.close()


if __name__ == "__main__":
    main()