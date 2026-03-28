# tools/climate.py — Climate tools: outdoor weather/air quality and indoor sensors
from datetime import datetime, timedelta

from core.tool_registry import mcp
from models import Nilu, Vindstyrka, Yr


@mcp.tool(
    description=(
        "Outdoor weather conditions (Yr: temperature, humidity, wind) "
        "and air quality measurements (NILU: PM10, PM2.5, NO2)."
    )
)
def get_outdoor_conditions(days: int = 7) -> dict:
    since = datetime.now() - timedelta(days=days)
    weather = list(
        Yr.select().where(Yr.record_time >= since).order_by(Yr.record_time.desc()).dicts()
    )
    air_quality = list(
        Nilu.select()
        .where(Nilu.record_time >= since)
        .order_by(Nilu.record_time.desc())
        .dicts()
    )
    return {"weather": weather, "air_quality": air_quality}


@mcp.tool(
    description=(
        "Indoor temperature, humidity, and air quality from Vindstyrka sensors. "
        "May include multiple sensors identified by sensor_name."
    )
)
def get_indoor_climate(days: int = 7) -> list[dict]:
    since = datetime.now() - timedelta(days=days)
    return list(
        Vindstyrka.select()
        .where(Vindstyrka.record_time >= since)
        .order_by(Vindstyrka.record_time.desc())
        .dicts()
    )
