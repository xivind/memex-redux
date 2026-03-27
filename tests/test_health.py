# tests/test_health.py
import pytest
from datetime import date, datetime, timedelta
from models import (
    PolarSleepDaily, PolarNightlyRecharge,
    PolarCardioLoad, PolarDailyActivity,
    Strava, Fitbit,
)

USER_ID = 123456789


def _polar_sleep(d, **kwargs):
    defaults = dict(
        polar_user_id=USER_ID, date=str(d), data_source="polar",
        created_at=f"{d} 08:00:00", updated_at=f"{d} 08:00:00",
        sleep_score=80, total_sleep_time=420,
    )
    defaults.update(kwargs)
    PolarSleepDaily.create(**defaults)


def _polar_recharge(d, **kwargs):
    defaults = dict(
        polar_user_id=USER_ID, date=str(d), data_source="polar",
        created_at=f"{d} 08:00:00", updated_at=f"{d} 08:00:00",
        ans_charge=75.0, nightly_recharge_status=2,
    )
    defaults.update(kwargs)
    PolarNightlyRecharge.create(**defaults)


def _polar_cardio(d, **kwargs):
    defaults = dict(
        polar_user_id=USER_ID, date=str(d), data_source="polar",
        created_at=f"{d} 08:00:00", updated_at=f"{d} 08:00:00",
        cardio_load=45.0, cardio_load_status="OPTIMAL",
    )
    defaults.update(kwargs)
    PolarCardioLoad.create(**defaults)


def _polar_activity(d, **kwargs):
    defaults = dict(
        polar_user_id=USER_ID, date=str(d), data_source="polar",
        created_at=f"{d} 08:00:00", updated_at=f"{d} 08:00:00",
        total_steps=8000, total_calories=2200,
    )
    defaults.update(kwargs)
    PolarDailyActivity.create(**defaults)


def test_get_sleep_combines_sleep_and_recharge(db_session):
    from tools.health import get_sleep
    today = date.today()
    _polar_sleep(today)
    _polar_recharge(today)
    result = get_sleep(days=7)
    assert len(result) == 1
    entry = result[0]
    assert "sleep_score" in entry
    assert "ans_charge" in entry
    assert entry["sleep_score"] == 80
    assert entry["ans_charge"] == pytest.approx(75.0)


def test_get_sleep_filters_by_days(db_session):
    from tools.health import get_sleep
    today = date.today()
    _polar_sleep(today)
    _polar_sleep(today - timedelta(days=20))
    result = get_sleep(days=7)
    assert len(result) == 1


def test_get_sleep_sleep_only_no_recharge(db_session):
    from tools.health import get_sleep
    today = date.today()
    _polar_sleep(today)
    result = get_sleep(days=7)
    assert len(result) == 1
    assert "sleep_score" in result[0]
    assert "ans_charge" not in result[0]


def test_get_training_combines_cardio_and_activity(db_session):
    from tools.health import get_training
    today = date.today()
    _polar_cardio(today)
    _polar_activity(today)
    result = get_training(days=7)
    assert len(result) == 1
    assert result[0]["cardio_load"] == pytest.approx(45.0)
    assert result[0]["total_steps"] == 8000


def test_get_training_filters_by_days(db_session):
    from tools.health import get_training
    today = date.today()
    _polar_cardio(today)
    _polar_cardio(today - timedelta(days=20))
    result = get_training(days=7)
    assert len(result) == 1


def test_get_strava_returns_recent_activities(db_session):
    from tools.health import get_strava
    today = datetime.now()
    Strava.create(
        id=1001, gear_id="b123", name="Morning Run", type="Run",
        location_country="Norway", start_date_local=str(today),
        elapsed_time="00:45:00", moving_time="00:43:00",
        distance=8500.0, average_speed=3.3, max_speed=4.1,
        total_elevation_gain=50, achievement_count=2,
        kudos_count=5, commute=False,
        average_heartrate=155, max_heartrate=172, suffer_score=42,
    )
    Strava.create(
        id=1002, gear_id="b123", name="Old Run", type="Run",
        location_country="Norway",
        start_date_local=str(today - timedelta(days=100)),
        elapsed_time="00:30:00", moving_time="00:29:00",
        distance=5000.0, average_speed=2.9, max_speed=3.5,
        total_elevation_gain=20, achievement_count=0,
        kudos_count=1, commute=False,
    )
    result = get_strava(days=30)
    assert len(result) == 1
    assert result[0]["name"] == "Morning Run"


def test_get_fitbit_returns_recent_rows(db_session):
    from tools.health import get_fitbit
    today = date.today()
    Fitbit.create(record_time=str(today), activity_steps=9500, heartrate_resting=58)
    Fitbit.create(
        record_time=str(today - timedelta(days=40)),
        activity_steps=7000, heartrate_resting=60,
    )
    result = get_fitbit(days=30)
    assert len(result) == 1
    assert result[0]["activity_steps"] == 9500
