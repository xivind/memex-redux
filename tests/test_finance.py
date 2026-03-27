# tests/test_finance.py
import pytest
from datetime import date, timedelta
from models import (
    Balance, Transaction,
    MoneybagCategory, MoneybagPayee,
    MoneybagBudgetEntry, MoneybagSupersaverCategory,
    MoneybagSupersaver, MoneybagTransaction,
)


def test_get_transactions_returns_recent_rows(db_session):
    from tools.finance import get_transactions
    today = date.today()
    Balance.create(
        record_time=f"{today} 10:00:00",
        balance=50000.0,
        account="Checking",
        card_provider="DNB",
    )
    Transaction.create(
        unique_id="t001",
        record_time=str(today),
        merchant_name="Kiwi",
        merchant_category="Groceries",
        amount=-89,
        card_provider="DNB",
        booking_status="BOOKED",
    )
    Transaction.create(
        unique_id="t002",
        record_time=str(today - timedelta(days=40)),
        merchant_name="Old transaction",
        merchant_category="Other",
        amount=-50,
        card_provider="DNB",
        booking_status="BOOKED",
    )
    result = get_transactions(days=30)
    assert "current_balance" in result
    assert result["current_balance"]["balance"] == pytest.approx(50000.0)
    assert len(result["transactions"]) == 1
    assert result["transactions"][0]["merchant_name"] == "Kiwi"


def test_get_transactions_no_balance(db_session):
    from tools.finance import get_transactions
    result = get_transactions(days=30)
    assert result["current_balance"] is None
    assert result["transactions"] == []


def test_get_budget_returns_budget_and_transactions(db_session):
    from tools.finance import get_budget
    cat = MoneybagCategory.create(
        id="cat01", created_at="2026-01-01 00:00:00", name="Food", type="expense"
    )
    payee = MoneybagPayee.create(
        id="pay01", created_at="2026-01-01 00:00:00", name="Rema", type="store"
    )
    MoneybagBudgetEntry.create(
        id="be01", created_at="2026-01-01 00:00:00",
        category=cat, year=2026, month=3, amount=4000,
        updated_at="2026-01-01 00:00:00", comment=None,
    )
    MoneybagTransaction.create(
        id="mt01", created_at="2026-03-15 00:00:00",
        category=cat, payee=payee, date="2026-03-15",
        amount=-350, comment=None, updated_at="2026-03-15 00:00:00",
    )
    result = get_budget(year=2026, month=3)
    assert result["period"] == "2026-03"
    assert len(result["budget"]) == 1
    assert result["budget"][0]["category"] == "Food"
    assert result["budget"][0]["budgeted"] == 4000
    assert len(result["transactions"]) == 1
    assert result["transactions"][0]["payee"] == "Rema"
    assert result["transactions"][0]["amount"] == -350


def test_get_budget_transaction_with_no_payee(db_session):
    from tools.finance import get_budget
    cat = MoneybagCategory.create(
        id="cat01", created_at="2026-01-01 00:00:00", name="Transport", type="expense"
    )
    MoneybagTransaction.create(
        id="mt01", created_at="2026-03-20 00:00:00",
        category=cat, payee=None, date="2026-03-20",
        amount=-200, comment="Bus", updated_at="2026-03-20 00:00:00",
    )
    result = get_budget(year=2026, month=3)
    assert result["transactions"][0]["payee"] is None


def test_get_budget_savings(db_session):
    from tools.finance import get_budget
    scat = MoneybagSupersaverCategory.create(
        id="sc01", name="Emergency fund",
        created_at="2026-01-01 00:00:00", updated_at="2026-01-01 00:00:00",
    )
    MoneybagSupersaver.create(
        id="ss01", category=scat, amount=2000, date="2026-03-10",
        comment=None, created_at="2026-03-10 00:00:00", updated_at="2026-03-10 00:00:00",
    )
    result = get_budget(year=2026, month=3)
    assert len(result["savings"]) == 1
    assert result["savings"][0]["amount"] == 2000
    assert result["savings"][0]["category"] == "Emergency fund"
