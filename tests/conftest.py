# tests/conftest.py
import peewee
import pytest
from unittest.mock import patch


@pytest.fixture
def no_db():
    """Prevent real DB calls during server tests."""
    with patch("core.db_connection.check_db_connection", return_value=False):
        yield


def _get_all_models():
    from models import (
        Balance, Transaction,
        MoneybagCategory, MoneybagPayee, MoneybagBudgetEntry,
        MoneybagBudgetTemplate, MoneybagConfiguration,
        MoneybagSupersaverCategory, MoneybagSupersaver, MoneybagTransaction,
        Fitbit, PolarSleepDaily, PolarNightlyRecharge,
        PolarCardioLoad, PolarDailyActivity, Strava,
        Nilu, Yr, Vindstyrka,
    )
    # Order matters: referenced tables before tables with FK constraints
    return [
        Balance, Transaction,
        MoneybagCategory, MoneybagPayee,
        MoneybagBudgetEntry, MoneybagBudgetTemplate, MoneybagConfiguration,
        MoneybagSupersaverCategory, MoneybagSupersaver, MoneybagTransaction,
        Fitbit, PolarSleepDaily, PolarNightlyRecharge,
        PolarCardioLoad, PolarDailyActivity, Strava,
        Nilu, Yr, Vindstyrka,
    ]


@pytest.fixture
def db_session():
    """SQLite in-memory DB with all tables created. Binds all models to test DB."""
    all_models = _get_all_models()
    test_db = peewee.SqliteDatabase(":memory:")
    with test_db.bind_ctx(all_models):
        test_db.create_tables(all_models)
        yield test_db
        test_db.drop_tables(all_models)
