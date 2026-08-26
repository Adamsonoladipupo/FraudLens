from fastapi import APIRouter

from app.db.cognodb import cognodb


router = APIRouter(
    prefix="/api/transactions",
    tags=["Transactions"],
)


@router.get("")
async def get_transactions():
    query = """
    MATCH (t:Transaction)

    RETURN
        t.id AS id,
        t.amount AS amount,
        t.currency AS currency,
        t.riskScore AS riskScore,
        t.transactionType AS transactionType,
        t.status AS status,
        t.timestamp AS timestamp

    ORDER BY t.timestamp DESC

    LIMIT 50
    """

    return cognodb.execute_query(query)