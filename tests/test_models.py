# tests/test_models.py
import pytest
from tests.conftest import _get_all_models
from models import (
    Balance, Transaction,
    MoneybagCategory, MoneybagPayee, MoneybagBudgetEntry,
    MoneybagBudgetTemplate, MoneybagConfiguration,
    MoneybagSupersaverCategory, MoneybagSupersaver, MoneybagTransaction,
    Fitbit, PolarSleepDaily, PolarNightlyRecharge,
    PolarCardioLoad, PolarDailyActivity, Strava,
    Nilu, Yr, Vindstyrka,
)


def test_all_tables_created(db_session):
    tables = db_session.get_tables()
    expected = {
        "balance", "transactions",
        "moneybags_categories", "moneybags_payees",
        "moneybags_budget_entries", "moneybags_budget_templates",
        "moneybags_configuration",
        "moneybags_supersaver_categories", "moneybags_supersaver",
        "moneybags_transactions",
        "fitbit", "polar_sleep_daily", "polar_nightly_recharge",
        "polar_cardio_load", "polar_daily_activity", "strava",
        "nilu", "yr", "vindstyrka",
    }
    assert expected.issubset(set(tables))


def test_balance_insert_and_query(db_session):
    Balance.create(
        record_time="2026-03-27 10:00:00",
        balance=12345.67,
        account="Checking",
        card_provider="DNB",
    )
    assert Balance.select().count() == 1
    row = Balance.get()
    assert row.balance == pytest.approx(12345.67)


def test_transaction_no_pk(db_session):
    Transaction.create(
        unique_id="abc123",
        record_time="2026-03-27",
        merchant_name="Rema",
        merchant_category="Groceries",
        amount=-150,
        card_provider="DNB",
        booking_status="BOOKED",
    )
    assert Transaction.select().count() == 1


def test_moneybag_fk_relationship(db_session):
    cat = MoneybagCategory.create(
        id="cat01",
        created_at="2026-01-01 00:00:00",
        name="Food",
        type="expense",
    )
    MoneybagBudgetEntry.create(
        id="be01",
        created_at="2026-01-01 00:00:00",
        category=cat,
        year=2026,
        month=3,
        amount=5000,
        updated_at="2026-01-01 00:00:00",
        comment=None,
    )
    entry = MoneybagBudgetEntry.get()
    assert entry.category.name == "Food"


def test_polar_composite_pk(db_session):
    PolarSleepDaily.create(
        polar_user_id=123456,
        date="2026-03-27",
        data_source="polar",
        created_at="2026-03-27 08:00:00",
        updated_at="2026-03-27 08:00:00",
    )
    assert PolarSleepDaily.select().count() == 1


def test_yr_no_pk_multiple_rows(db_session):
    Yr.create(
        record_time="2026-03-27 10:00:00",
        location="Oslo",
        air_temperature=5,
        relative_humidity=70,
        wind_from_direction=180,
        wind_speed=3,
    )
    Yr.create(
        record_time="2026-03-27 11:00:00",
        location="Oslo",
        air_temperature=6,
        relative_humidity=68,
        wind_from_direction=180,
        wind_speed=4,
    )
    assert Yr.select().count() == 2
