# tools/strava.py — Strava activity tools
import json
import os
import peewee
from datetime import datetime, timedelta

from core.tool_registry import mcp
from models import Strava

_GEAR_FILE = os.path.join(os.path.dirname(__file__), "..", "gear.json")


def _load_gear() -> dict:
    try:
        with open(_GEAR_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _query_strava_summary(since: datetime, activity_type: str | None) -> list[dict]:
    gear = _load_gear()
    query = Strava.select().where(Strava.start_date_local >= since)
    if activity_type:
        query = query.where(Strava.type == activity_type)

    groups: dict[tuple, dict] = {}
    for a in query:
        iso = a.start_date_local.isocalendar()
        week = f"{iso[0]}-W{iso[1]:02d}"
        gear_name = gear.get(a.gear_id, a.gear_id)
        key = (week, a.type, gear_name)
        if key not in groups:
            groups[key] = {"count": 0, "distance": 0.0, "elevation": 0, "speed_sum": 0.0, "hr_sum": 0, "hr_count": 0}
        g = groups[key]
        g["count"] += 1
        g["distance"] += a.distance
        g["elevation"] += a.total_elevation_gain
        g["speed_sum"] += a.average_speed
        if a.average_heartrate:
            g["hr_sum"] += a.average_heartrate
            g["hr_count"] += 1

    result = []
    for (week, atype, gear_name), g in sorted(groups.items(), key=lambda x: x[0][0], reverse=True):
        result.append({
            "week": week,
            "activity_type": atype,
            "gear": gear_name,
            "count": g["count"],
            "total_distance_km": round(g["distance"] / 1000, 1),
            "total_elevation_m": g["elevation"],
            "avg_speed_kmh": round((g["speed_sum"] / g["count"]) * 3.6, 1),
            "avg_heartrate": round(g["hr_sum"] / g["hr_count"]) if g["hr_count"] else None,
        })
    return result


def _query_strava_activities(since: datetime, activity_type: str | None) -> list[dict]:
    gear = _load_gear()
    query = (
        Strava.select()
        .where(Strava.start_date_local >= since)
        .order_by(Strava.start_date_local.desc())
    )
    if activity_type:
        query = query.where(Strava.type == activity_type)

    result = []
    for a in query:
        result.append({
            "id": a.id,
            "date": str(a.start_date_local),
            "name": a.name,
            "type": a.type,
            "gear": gear.get(a.gear_id, a.gear_id),
            "gear_id": a.gear_id,
            "distance_km": round(a.distance / 1000, 2),
            "moving_time": str(a.moving_time),
            "elapsed_time": str(a.elapsed_time),
            "elevation_m": a.total_elevation_gain,
            "avg_speed_kmh": round(a.average_speed * 3.6, 1),
            "max_speed_kmh": round(a.max_speed * 3.6, 1),
            "avg_heartrate": a.average_heartrate,
            "max_heartrate": a.max_heartrate,
            "suffer_score": a.suffer_score,
            "commute": a.commute,
            "location_country": a.location_country,
            "achievement_count": a.achievement_count,
            "kudos_count": a.kudos_count,
        })
    return result


@mcp.tool(
    description=(
        "Weekly training summary from Strava for the last 30 days, grouped by activity type and bike/gear. "
        "Returns activity count, total distance, total elevation, and average speed per week. "
        "Optionally filter by activity_type (e.g. 'Ride', 'Run', 'Walk')."
    )
)
def get_strava_summary_30d(activity_type: str | None = None) -> list[dict]:
    return _query_strava_summary(datetime.now() - timedelta(days=30), activity_type)


@mcp.tool(
    description=(
        "Weekly training summary from Strava for the last 90 days, grouped by activity type and bike/gear. "
        "Returns activity count, total distance, total elevation, and average speed per week. "
        "Optionally filter by activity_type (e.g. 'Ride', 'Run', 'Walk')."
    )
)
def get_strava_summary_90d(activity_type: str | None = None) -> list[dict]:
    return _query_strava_summary(datetime.now() - timedelta(days=90), activity_type)


@mcp.tool(
    description=(
        "Recent Strava activities with full detail including bike/gear name, for the last 30 days. "
        "Optionally filter by activity_type (e.g. 'Ride', 'Run', 'Walk')."
    )
)
def get_strava_activities_30d(activity_type: str | None = None) -> list[dict]:
    return _query_strava_activities(datetime.now() - timedelta(days=30), activity_type)


@mcp.tool(
    description=(
        "Recent Strava activities with full detail including bike/gear name, for the last 90 days. "
        "Optionally filter by activity_type (e.g. 'Ride', 'Run', 'Walk')."
    )
)
def get_strava_activities_90d(activity_type: str | None = None) -> list[dict]:
    return _query_strava_activities(datetime.now() - timedelta(days=90), activity_type)
