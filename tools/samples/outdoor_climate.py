# tools/outdoor_climate.py — Outdoor weather from Yr (city location)
import peewee
from datetime import datetime, timedelta

from core.tool_registry import mcp
from models import Yr


def _query_outdoor(since: datetime) -> list[dict]:
    return list(
        Yr.select(
            peewee.fn.DATE(Yr.record_time).alias("date"),
            peewee.fn.MIN(Yr.air_temperature).alias("air_temperature_min"),
            peewee.fn.MAX(Yr.air_temperature).alias("air_temperature_max"),
            peewee.fn.MIN(Yr.relative_humidity).alias("relative_humidity_min"),
            peewee.fn.MAX(Yr.relative_humidity).alias("relative_humidity_max"),
            peewee.fn.MIN(Yr.wind_from_direction).alias("wind_from_direction_min"),
            peewee.fn.MAX(Yr.wind_from_direction).alias("wind_from_direction_max"),
            peewee.fn.MIN(Yr.wind_speed).alias("wind_speed_min"),
            peewee.fn.MAX(Yr.wind_speed).alias("wind_speed_max"),
        )
        .where((Yr.record_time >= since) & (Yr.location == "city"))
        .group_by(peewee.fn.DATE(Yr.record_time))
        .order_by(peewee.fn.DATE(Yr.record_time).desc())
        .dicts()
    )


@mcp.tool(
    description=(
        "Outdoor weather in the city for the last 30 days from Yr. "
        "Returns daily min/max for air temperature, relative humidity, "
        "wind direction, and wind speed."
    )
)
def get_outdoor_climate_30d() -> list[dict]:
    return _query_outdoor(datetime.now() - timedelta(days=30))


@mcp.tool(
    description=(
        "Outdoor weather in the city for the last 90 days from Yr. "
        "Returns daily min/max for air temperature, relative humidity, "
        "wind direction, and wind speed."
    )
)
def get_outdoor_climate_90d() -> list[dict]:
    return _query_outdoor(datetime.now() - timedelta(days=90))
