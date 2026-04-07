# tools/air_pollution.py — Outdoor air quality from NILU (Oslo)
import peewee
from datetime import datetime, timedelta

from core.tool_registry import mcp
from models import Nilu


def _query_air_pollution(since: datetime) -> list[dict]:
    return list(
        Nilu.select(
            peewee.fn.DATE(Nilu.record_time).alias("date"),
            peewee.fn.MIN(Nilu.airquality_pm10).alias("pm10_min"),
            peewee.fn.MAX(Nilu.airquality_pm10).alias("pm10_max"),
            peewee.fn.MIN(Nilu.airquality_pm25).alias("pm25_min"),
            peewee.fn.MAX(Nilu.airquality_pm25).alias("pm25_max"),
            peewee.fn.MIN(Nilu.airquality_no2).alias("no2_min"),
            peewee.fn.MAX(Nilu.airquality_no2).alias("no2_max"),
        )
        .where(Nilu.record_time >= since)
        .group_by(peewee.fn.DATE(Nilu.record_time))
        .order_by(peewee.fn.DATE(Nilu.record_time).desc())
        .dicts()
    )


@mcp.tool(
    description=(
        "Outdoor air quality in Oslo for the last 30 days from NILU. "
        "Returns daily min/max for PM10, PM2.5, and NO2. "
        "For indoor air pollution cross-reference, note that Vindstyrka sensors measure PM2.5 only."
    )
)
def get_air_pollution_30d() -> list[dict]:
    return _query_air_pollution(datetime.now() - timedelta(days=30))


@mcp.tool(
    description=(
        "Outdoor air quality in Oslo for the last 90 days from NILU. "
        "Returns daily min/max for PM10, PM2.5, and NO2. "
        "For indoor air pollution cross-reference, note that Vindstyrka sensors measure PM2.5 only."
    )
)
def get_air_pollution_90d() -> list[dict]:
    return _query_air_pollution(datetime.now() - timedelta(days=90))
