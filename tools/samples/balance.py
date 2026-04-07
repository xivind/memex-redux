# tools/balance.py — Account balance data
from datetime import date, timedelta

from core.tool_registry import mcp
from models import Balance


def _query_balance(since: date) -> list[dict]:
    return list(
        Balance.select(Balance.record_time, Balance.balance, Balance.account)
        .where(Balance.record_time >= since)
        .order_by(Balance.record_time.desc())
        .dicts()
    )


@mcp.tool(
    description="Account balance for the last 30 days."
)
def get_balance_30d() -> list[dict]:
    return _query_balance(date.today() - timedelta(days=30))


@mcp.tool(
    description="Account balance for the last 90 days."
)
def get_balance_90d() -> list[dict]:
    return _query_balance(date.today() - timedelta(days=90))
