# tools/health.py — Health tools: Polar sleep/training, Strava, Fitbit
from datetime import date, datetime, timedelta

from core.tool_registry import mcp
from models import Fitbit, PolarCardioLoad, PolarDailyActivity, PolarNightlyRecharge, PolarSleepDaily, Strava


@mcp.tool(
    description=(
        "Sleep duration, quality scores, and nightly recovery metrics from Polar. "
        "Combines polar_sleep_daily and polar_nightly_recharge by date. "
        "Default is 14 days — increase for trend analysis or decrease for a quick recent check."
    )
)
def get_sleep(days: int = 14) -> list[dict]:
    since = date.today() - timedelta(days=days)
    sleep_map = {
        row.date: row
        for row in PolarSleepDaily.select().where(PolarSleepDaily.date >= since)
    }
    recharge_map = {
        row.date: row
        for row in PolarNightlyRecharge.select().where(PolarNightlyRecharge.date >= since)
    }
    all_dates = sorted(set(sleep_map) | set(recharge_map), reverse=True)
    result = []
    for d in all_dates:
        entry = {"date": str(d)}
        s = sleep_map.get(d)
        if s:
            # polar_user_id, data_source, created_at, updated_at excluded (metadata, not health data)
            entry.update(
                {
                    "sleep_score": s.sleep_score,
                    "total_sleep_time": s.total_sleep_time,
                    "light_sleep": s.light_sleep,
                    "deep_sleep": s.deep_sleep,
                    "rem_sleep": s.rem_sleep,
                    "sleep_start_time": s.sleep_start_time,
                    "sleep_end_time": s.sleep_end_time,
                    "sleep_charge": s.sleep_charge,
                    "sleep_rating": s.sleep_rating,
                    "continuity": s.continuity,
                    "continuity_class": s.continuity_class,
                    "sleep_cycles": s.sleep_cycles,
                    "total_interruption_duration": s.total_interruption_duration,
                    "short_interruption_duration": s.short_interruption_duration,
                    "long_interruption_duration": s.long_interruption_duration,
                    "sleep_goal": s.sleep_goal,
                    "group_duration_score": s.group_duration_score,
                    "group_solidity_score": s.group_solidity_score,
                    "group_regeneration_score": s.group_regeneration_score,
                }
            )
        r = recharge_map.get(d)
        if r:
            entry.update(
                {
                    "ans_charge": r.ans_charge,
                    "ans_charge_status": r.ans_charge_status,
                    "nightly_recharge_status": r.nightly_recharge_status,
                    "heart_rate_variability_avg": r.heart_rate_variability_avg,
                    "heart_rate_avg": r.heart_rate_avg,
                    "breathing_rate_avg": r.breathing_rate_avg,
                    "beat_to_beat_avg": r.beat_to_beat_avg,
                    "hrv_samples_count": r.hrv_samples_count,
                    "breathing_samples_count": r.breathing_samples_count,
                }
            )
        result.append(entry)
    return result


@mcp.tool(
    description=(
        "Training load, cardio stress, and daily activity data from Polar. "
        "Combines polar_cardio_load and polar_daily_activity by date. "
        "Default is 14 days — increase for trend analysis or decrease for a quick recent check."
    )
)
def get_training(days: int = 14) -> list[dict]:
    since = date.today() - timedelta(days=days)
    cardio_map = {
        row.date: row
        for row in PolarCardioLoad.select().where(PolarCardioLoad.date >= since)
    }
    activity_map = {
        row.date: row
        for row in PolarDailyActivity.select().where(PolarDailyActivity.date >= since)
    }
    all_dates = sorted(set(cardio_map) | set(activity_map), reverse=True)
    result = []
    for d in all_dates:
        entry = {"date": str(d)}
        c = cardio_map.get(d)
        if c:
            # polar_user_id, data_source, created_at, updated_at excluded (metadata, not health data)
            entry.update(
                {
                    "cardio_load": c.cardio_load,
                    "cardio_load_status": c.cardio_load_status,
                    "cardio_load_ratio": c.cardio_load_ratio,
                    "strain": c.strain,
                    "tolerance": c.tolerance,
                    "level_very_low": c.level_very_low,
                    "level_low": c.level_low,
                    "level_medium": c.level_medium,
                    "level_high": c.level_high,
                    "level_very_high": c.level_very_high,
                }
            )
        a = activity_map.get(d)
        if a:
            entry.update(
                {
                    "total_calories": a.total_calories,
                    "active_calories": a.active_calories,
                    "total_steps": a.total_steps,
                    "total_duration": a.total_duration,
                    "activity_count": a.activity_count,
                }
            )
        result.append(entry)
    return result


@mcp.tool(
    description=(
        "Strava workout activities including runs, rides, distance, elevation, "
        "and heart rate. Default is 90 days — adjust based on the question, "
        "but prefer focused ranges as this is a large dataset."
    )
)
def get_strava(days: int = 90) -> list[dict]:
    since = datetime.now() - timedelta(days=days)
    return list(
        Strava.select()
        .where(Strava.start_date_local >= since)
        .order_by(Strava.start_date_local.desc())
        .dicts()
    )


@mcp.tool(
    description=(
        "Fitbit health metrics: steps, calories, sleep stages, heart rate zones, "
        "HRV, SpO2, skin temperature, and weight. "
        "Default is 30 days — increase for longer trend analysis or decrease for recent data only."
    )
)
def get_fitbit(days: int = 30) -> list[dict]:
    since = date.today() - timedelta(days=days)
    return list(
        Fitbit.select()
        .where(Fitbit.record_time >= since)
        .order_by(Fitbit.record_time.desc())
        .dicts()
    )
