# tools/sleep.py — Sleep data from Polar
from datetime import date, timedelta

from core.tool_registry import mcp
from models import PolarNightlyRecharge, PolarSleepDaily


def _query_sleep(since: date) -> list[dict]:
    recharge_map = {
        row.date: row
        for row in PolarNightlyRecharge.select(
            PolarNightlyRecharge.date,
            PolarNightlyRecharge.heart_rate_avg,
            PolarNightlyRecharge.heart_rate_variability_avg,
            PolarNightlyRecharge.breathing_rate_avg,
            PolarNightlyRecharge.ans_charge,
        ).where(PolarNightlyRecharge.date >= since)
    }
    sleep_map = {
        row.date: row
        for row in PolarSleepDaily.select(
            PolarSleepDaily.date,
            PolarSleepDaily.sleep_start_time,
            PolarSleepDaily.sleep_end_time,
            PolarSleepDaily.light_sleep,
            PolarSleepDaily.deep_sleep,
            PolarSleepDaily.rem_sleep,
            PolarSleepDaily.total_sleep_time,
            PolarSleepDaily.sleep_score,
        ).where(PolarSleepDaily.date >= since)
    }
    all_dates = sorted(set(recharge_map) | set(sleep_map), reverse=True)
    result = []
    for d in all_dates:
        entry = {"date": str(d)}
        r = recharge_map.get(d)
        if r:
            entry.update({
                "heart_rate_avg": r.heart_rate_avg,
                "heart_rate_variability_avg": r.heart_rate_variability_avg,
                "breathing_rate_avg": r.breathing_rate_avg,
                "ans_charge": r.ans_charge,
            })
        s = sleep_map.get(d)
        if s:
            entry.update({
                "sleep_start_time": s.sleep_start_time,
                "sleep_end_time": s.sleep_end_time,
                "light_sleep": s.light_sleep,
                "deep_sleep": s.deep_sleep,
                "rem_sleep": s.rem_sleep,
                "total_sleep_time": s.total_sleep_time,
                "sleep_score": s.sleep_score,
            })
        result.append(entry)
    return result


@mcp.tool(
    description=(
        "Nightly sleep duration, stages, score, and recovery metrics from Polar for the last 30 days."
    )
)
def get_sleep_30d() -> list[dict]:
    return _query_sleep(date.today() - timedelta(days=30))


@mcp.tool(
    description=(
        "Nightly sleep duration, stages, score, and recovery metrics from Polar for the last 90 days."
    )
)
def get_sleep_90d() -> list[dict]:
    return _query_sleep(date.today() - timedelta(days=90))
