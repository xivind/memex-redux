# tools/transactions.py — Card transaction data
from datetime import date, timedelta

from core.tool_registry import mcp
from models import Transaction


def _query_transactions(since: date) -> list[dict]:
    return list(
        Transaction.select(
            Transaction.record_time,
            Transaction.merchant_name,
            Transaction.merchant_category,
            Transaction.amount,
        )
        .where(Transaction.record_time >= since)
        .order_by(Transaction.record_time.desc())
        .dicts()
    )


@mcp.tool(
    description=(
        "Card transactions for the last 30 days including merchant name, category, and amount."
    )
)
def get_transactions_30d() -> list[dict]:
    return _query_transactions(date.today() - timedelta(days=30))


@mcp.tool(
    description=(
        "Card transactions for the last 90 days including merchant name, category, and amount."
    )
)
def get_transactions_90d() -> list[dict]:
    return _query_transactions(date.today() - timedelta(days=90))
