# tools/weight.py — Weight data from Fitbit
from datetime import date, timedelta

from core.tool_registry import mcp
from models import Fitbit


def _query_weight(since: date) -> list[dict]:
    return list(
        Fitbit.select(Fitbit.record_time, Fitbit.weight_weight, Fitbit.weight_bmi)
        .where(
            (Fitbit.record_time >= since)
            & (Fitbit.weight_weight.is_null(False))
        )
        .order_by(Fitbit.record_time.desc())
        .dicts()
    )


@mcp.tool(
    description=(
        "Body weight and BMI for the last 30 days from Fitbit."
    )
)
def get_weight_30d() -> list[dict]:
    return _query_weight(date.today() - timedelta(days=30))


@mcp.tool(
    description=(
        "Body weight and BMI for the last 90 days from Fitbit."
    )
)
def get_weight_90d() -> list[dict]:
    return _query_weight(date.today() - timedelta(days=90))
