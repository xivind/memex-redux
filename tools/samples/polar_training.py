# tools/polar_training.py — Training data from Polar
from datetime import date, timedelta

from core.tool_registry import mcp
from models import PolarCardioLoad, PolarDailyActivity


def _query_polar_training(since: date) -> list[dict]:
    cardio_map = {
        row.date: row.cardio_load_status
        for row in PolarCardioLoad.select(PolarCardioLoad.date, PolarCardioLoad.cardio_load_status)
        .where(PolarCardioLoad.date >= since)
    }
    activity_map = {
        row.date: row.total_calories
        for row in PolarDailyActivity.select(PolarDailyActivity.date, PolarDailyActivity.total_calories)
        .where(PolarDailyActivity.date >= since)
    }
    all_dates = sorted(set(cardio_map) | set(activity_map), reverse=True)
    return [
        {
            "date": str(d),
            "cardio_load_status": cardio_map.get(d),
            "total_calories": activity_map.get(d),
        }
        for d in all_dates
    ]


@mcp.tool(
    description=(
        "Daily training load status and calorie burn from Polar for the last 30 days."
    )
)
def get_polar_training_30d() -> list[dict]:
    return _query_polar_training(date.today() - timedelta(days=30))


@mcp.tool(
    description=(
        "Daily training load status and calorie burn from Polar for the last 90 days."
    )
)
def get_polar_training_90d() -> list[dict]:
    return _query_polar_training(date.today() - timedelta(days=90))
