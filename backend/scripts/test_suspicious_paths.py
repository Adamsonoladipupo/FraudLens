from app.db.cognodb import cognodb
from app.repositories.investigation_repository import (
    InvestigationRepository,
)


def main():
    cognodb.connect()

    try:
        cognodb.verify_connection()

        repository = InvestigationRepository()

        transaction_id = "TXN-001"

        result = repository.get_suspicious_paths(
            transaction_id
        )

        print("\nSuspicious paths:")
        print(result)

    finally:
        cognodb.close()


if __name__ == "__main__":
    main()