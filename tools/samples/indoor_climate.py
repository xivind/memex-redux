# tools/indoor_climate.py — Indoor climate from Vindstyrka sensors
import peewee
from datetime import datetime, timedelta

from core.tool_registry import mcp
from models import Vindstyrka


def _query_indoor(since: datetime) -> list[dict]:
    return list(
        Vindstyrka.select(
            peewee.fn.DATE(Vindstyrka.record_time).alias("date"),
            Vindstyrka.sensor_name,
            peewee.fn.MIN(Vindstyrka.temperature).alias("temp_min"),
            peewee.fn.MAX(Vindstyrka.temperature).alias("temp_max"),
            peewee.fn.MIN(Vindstyrka.humidity).alias("humidity_min"),
            peewee.fn.MAX(Vindstyrka.humidity).alias("humidity_max"),
            peewee.fn.MIN(Vindstyrka.air_pollution).alias("air_pollution_min"),
            peewee.fn.MAX(Vindstyrka.air_pollution).alias("air_pollution_max"),
        )
        .where(Vindstyrka.record_time >= since)
        .group_by(peewee.fn.DATE(Vindstyrka.record_time), Vindstyrka.sensor_name)
        .order_by(peewee.fn.DATE(Vindstyrka.record_time).desc(), Vindstyrka.sensor_name)
        .dicts()
    )


@mcp.tool(
    description=(
        "Indoor climate for the last 30 days from three Vindstyrka sensors "
        "(Sensor Verksted, Sensor Soverom, Sensor Stue). "
        "Returns daily min/max for temperature, humidity, and air pollution per sensor. "
        "Note: indoor air pollution measures PM2.5 only."
    )
)
def get_indoor_climate_30d() -> list[dict]:
    return _query_indoor(datetime.now() - timedelta(days=30))


@mcp.tool(
    description=(
        "Indoor climate for the last 90 days from three Vindstyrka sensors "
        "(Sensor Verksted, Sensor Soverom, Sensor Stue). "
        "Returns daily min/max for temperature, humidity, and air pollution per sensor. "
        "Note: indoor air pollution measures PM2.5 only."
    )
)
def get_indoor_climate_90d() -> list[dict]:
    return _query_indoor(datetime.now() - timedelta(days=90))
