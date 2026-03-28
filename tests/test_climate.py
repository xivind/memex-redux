# tests/test_climate.py
import pytest
from datetime import datetime, timedelta
from models import Yr, Nilu, Vindstyrka


def test_get_outdoor_conditions_returns_weather_and_air_quality(db_session):
    from tools.climate import get_outdoor_conditions
    now = datetime.now()
    Yr.create(
        record_time=str(now),
        location="Oslo",
        air_temperature=8,
        relative_humidity=65,
        wind_from_direction=270,
        wind_speed=5,
    )
    Nilu.create(
        record_time=str(now),
        airquality_pm10=12.5,
        airquality_pm25=8.1,
        airquality_no2=20.3,
    )
    result = get_outdoor_conditions(days=7)
    assert "weather" in result
    assert "air_quality" in result
    assert len(result["weather"]) == 1
    assert result["weather"][0]["air_temperature"] == 8
    assert len(result["air_quality"]) == 1
    assert result["air_quality"][0]["airquality_pm10"] == pytest.approx(12.5)


def test_get_outdoor_conditions_filters_by_days(db_session):
    from tools.climate import get_outdoor_conditions
    now = datetime.now()
    Yr.create(
        record_time=str(now), location="Oslo", air_temperature=5,
        relative_humidity=70, wind_from_direction=180, wind_speed=3,
    )
    Yr.create(
        record_time=str(now - timedelta(days=10)), location="Oslo", air_temperature=3,
        relative_humidity=80, wind_from_direction=90, wind_speed=6,
    )
    result = get_outdoor_conditions(days=7)
    assert len(result["weather"]) == 1


def test_get_outdoor_conditions_empty(db_session):
    from tools.climate import get_outdoor_conditions
    result = get_outdoor_conditions(days=7)
    assert result == {"weather": [], "air_quality": []}


def test_get_indoor_climate_returns_recent_rows(db_session):
    from tools.climate import get_indoor_climate
    now = datetime.now()
    Vindstyrka.create(
        record_time=str(now),
        sensor_name="Living room",
        temperature=21.5,
        humidity=45,
        air_pollution=3,
    )
    Vindstyrka.create(
        record_time=str(now - timedelta(days=10)),
        sensor_name="Living room",
        temperature=20.0,
        humidity=50,
        air_pollution=2,
    )
    result = get_indoor_climate(days=7)
    assert len(result) == 1
    assert result[0]["sensor_name"] == "Living room"
    assert result[0]["temperature"] == pytest.approx(21.5)


def test_get_indoor_climate_multiple_sensors(db_session):
    from tools.climate import get_indoor_climate
    now = datetime.now()
    Vindstyrka.create(
        record_time=str(now), sensor_name="Living room",
        temperature=21.5, humidity=45, air_pollution=3,
    )
    Vindstyrka.create(
        record_time=str(now - timedelta(hours=1)), sensor_name="Bedroom",
        temperature=19.0, humidity=55, air_pollution=2,
    )
    result = get_indoor_climate(days=1)
    assert len(result) == 2
