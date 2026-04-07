# tools/moneybags.py — Moneybags budgeting: budget plan and actual expenses
import peewee
from datetime import date, timedelta
import calendar

from core.tool_registry import mcp
from models import MoneybagBudgetEntry, MoneybagCategory, MoneybagPayee, MoneybagTransaction


# ---------------------------------------------------------------------------
# Date range helpers
# ---------------------------------------------------------------------------

def _current_month_range() -> tuple[date, date]:
    today = date.today()
    return date(today.year, today.month, 1), today


def _last_month_range() -> tuple[date, date]:
    today = date.today()
    end = date(today.year, today.month, 1) - timedelta(days=1)
    return date(end.year, end.month, 1), end


def _last_3_months_range() -> tuple[date, date]:
    today = date.today()
    end = date(today.year, today.month, 1) - timedelta(days=1)
    month = end.month - 2
    year = end.year
    if month <= 0:
        month += 12
        year -= 1
    return date(year, month, 1), end


def _ytd_range() -> tuple[date, date]:
    today = date.today()
    return date(today.year, 1, 1), today


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------

def _budget_for_period(start: date, end: date) -> list[dict]:
    start_key = start.year * 100 + start.month
    end_key = end.year * 100 + end.month
    result = []
    for entry in (
        MoneybagBudgetEntry.select(MoneybagBudgetEntry, MoneybagCategory)
        .join(MoneybagCategory)
        .where(
            (MoneybagBudgetEntry.year * 100 + MoneybagBudgetEntry.month).between(
                start_key, end_key
            )
        )
        .order_by(MoneybagBudgetEntry.year, MoneybagBudgetEntry.month)
    ):
        result.append({
            "year": entry.year,
            "month": entry.month,
            "category": entry.category.name,
            "category_type": entry.category.type,
            "budgeted": entry.amount,
            "comment": entry.comment,
        })
    return result


def _expenses_for_period(start: date, end: date) -> list[dict]:
    result = []
    for txn in (
        MoneybagTransaction.select(MoneybagTransaction, MoneybagCategory, MoneybagPayee)
        .join(MoneybagCategory)
        .switch(MoneybagTransaction)
        .join(MoneybagPayee, peewee.JOIN.LEFT_OUTER)
        .where(
            (MoneybagTransaction.date >= start) & (MoneybagTransaction.date <= end)
        )
        .order_by(MoneybagTransaction.date.desc())
    ):
        result.append({
            "date": str(txn.date),
            "category": txn.category.name,
            "category_type": txn.category.type,
            "payee": txn.payee.name if txn.payee_id else None,
            "amount": txn.amount,
            "comment": txn.comment,
        })
    return result


# ---------------------------------------------------------------------------
# Budget tools
# ---------------------------------------------------------------------------

@mcp.tool(
    description="Moneybags budget plan for the current month so far, by category."
)
def get_budget_current_month() -> list[dict]:
    return _budget_for_period(*_current_month_range())


@mcp.tool(
    description="Moneybags budget plan for last month, by category."
)
def get_budget_last_month() -> list[dict]:
    return _budget_for_period(*_last_month_range())


@mcp.tool(
    description="Moneybags budget plan for the last 3 completed months, by category."
)
def get_budget_last_3_months() -> list[dict]:
    return _budget_for_period(*_last_3_months_range())


@mcp.tool(
    description="Moneybags budget plan for the current year so far, by category."
)
def get_budget_ytd() -> list[dict]:
    return _budget_for_period(*_ytd_range())


# ---------------------------------------------------------------------------
# Expense tools
# ---------------------------------------------------------------------------

@mcp.tool(
    description="Moneybags actual expenses for the current month so far, with category and payee."
)
def get_expenses_current_month() -> list[dict]:
    return _expenses_for_period(*_current_month_range())


@mcp.tool(
    description="Moneybags actual expenses for last month, with category and payee."
)
def get_expenses_last_month() -> list[dict]:
    return _expenses_for_period(*_last_month_range())


@mcp.tool(
    description="Moneybags actual expenses for the last 3 completed months, with category and payee."
)
def get_expenses_last_3_months() -> list[dict]:
    return _expenses_for_period(*_last_3_months_range())


@mcp.tool(
    description="Moneybags actual expenses for the current year so far, with category and payee."
)
def get_expenses_ytd() -> list[dict]:
    return _expenses_for_period(*_ytd_range())
