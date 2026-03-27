# tools/finance.py — Finance tools: ATM provider data and Moneybags budgeting
import calendar
from datetime import date, timedelta

import peewee

from core.tool_registry import mcp
from models import (
    Balance,
    MoneybagBudgetEntry,
    MoneybagCategory,
    MoneybagPayee,
    MoneybagSupersaver,
    MoneybagSupersaverCategory,
    MoneybagTransaction,
    Transaction,
)


@mcp.tool(description="Recent bank transactions and current account balance from ATM provider")
def get_transactions(days: int = 30) -> dict:
    since = date.today() - timedelta(days=days)
    latest = Balance.select().order_by(Balance.record_time.desc()).first()
    current_balance = None
    if latest:
        current_balance = {
            "balance": latest.balance,
            "account": latest.account,
            "card_provider": latest.card_provider,
            "as_of": str(latest.record_time),
        }
    transactions = list(
        Transaction.select()
        .where(Transaction.record_time >= since)
        .order_by(Transaction.record_time.desc())
        .dicts()
    )
    return {"current_balance": current_balance, "transactions": transactions}


@mcp.tool(
    description=(
        "Budget plan vs actual spending from Moneybags budgeting system for a given month. "
        "Returns budgeted amounts by category, actual transactions, and savings deposits."
    )
)
def get_budget(year: int | None = None, month: int | None = None) -> dict:
    today = date.today()
    year = year or today.year
    month = month or today.month
    last_day = calendar.monthrange(year, month)[1]
    month_start = date(year, month, 1)
    month_end = date(year, month, last_day)

    budget = []
    for entry in (
        MoneybagBudgetEntry.select(MoneybagBudgetEntry, MoneybagCategory)
        .join(MoneybagCategory)
        .where(
            (MoneybagBudgetEntry.year == year) & (MoneybagBudgetEntry.month == month)
        )
    ):
        budget.append(
            {
                "category": entry.category.name,
                "category_type": entry.category.type,
                "budgeted": entry.amount,
                "comment": entry.comment,
            }
        )

    transactions = []
    for txn in (
        MoneybagTransaction.select(MoneybagTransaction, MoneybagCategory, MoneybagPayee)
        .join(MoneybagCategory)
        .switch(MoneybagTransaction)
        .join(MoneybagPayee, peewee.JOIN.LEFT_OUTER)
        .where(
            (MoneybagTransaction.date >= month_start)
            & (MoneybagTransaction.date <= month_end)
        )
        .order_by(MoneybagTransaction.date.desc())
    ):
        transactions.append(
            {
                "date": str(txn.date),
                "category": txn.category.name,
                "payee": txn.payee.name if txn.payee_id else None,
                "amount": txn.amount,
                "comment": txn.comment,
            }
        )

    savings = []
    for s in (
        MoneybagSupersaver.select(MoneybagSupersaver, MoneybagSupersaverCategory)
        .join(MoneybagSupersaverCategory)
        .where(
            (MoneybagSupersaver.date >= month_start)
            & (MoneybagSupersaver.date <= month_end)
        )
        .order_by(MoneybagSupersaver.date.desc())
    ):
        savings.append(
            {
                "date": str(s.date),
                "category": s.category.name,
                "amount": s.amount,
                "comment": s.comment,
            }
        )

    return {
        "period": f"{year}-{month:02d}",
        "budget": budget,
        "transactions": transactions,
        "savings": savings,
    }
