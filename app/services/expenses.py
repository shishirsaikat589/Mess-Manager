
from sqlalchemy import extract
from sqlalchemy.orm import Session

from app import models


def parse_month(month: str) -> tuple[int, int]:
    """Turns 'YYYY-MM' into (year, month) ints. Raises ValueError if malformed."""
    year_str, month_str = month.split("-")
    return int(year_str), int(month_str)


def calculate_settlement(db: Session, month: str) -> dict:
    year, mon = parse_month(month)

    # --- Pool totals for the month ---
    meals_this_month = (
        db.query(models.MealEntry)
        .filter(
            extract("year", models.MealEntry.date) == year,
            extract("month", models.MealEntry.date) == mon,
        )
        .all()
    )
    expenses_this_month = (
        db.query(models.Expense)
        .filter(
            extract("year", models.Expense.date) == year,
            extract("month", models.Expense.date) == mon,
        )
        .all()
    )
    deposits_this_month = (
        db.query(models.Deposit)
        .filter(
            extract("year", models.Deposit.date) == year,
            extract("month", models.Deposit.date) == mon,
        )
        .all()
    )

    total_meals = sum(m.meal_count for m in meals_this_month)
    total_expense = sum(e.amount for e in expenses_this_month)
    meal_rate = (total_expense / total_meals) if total_meals > 0 else 0.0

    # --- Per-user breakdown ---
    meals_by_user: dict[int, int] = {}
    for m in meals_this_month:
        meals_by_user[m.user_id] = meals_by_user.get(m.user_id, 0) + m.meal_count

    paid_by_user: dict[int, float] = {}
    for d in deposits_this_month:
        paid_by_user[d.user_id] = paid_by_user.get(d.user_id, 0.0) + d.amount

    # Every user who logged a meal OR made a deposit should appear in the report
    relevant_user_ids = set(meals_by_user) | set(paid_by_user)

    members = []
    for user_id in relevant_user_ids:
        user = db.get(models.User, user_id)
        user_meals = meals_by_user.get(user_id, 0)
        meal_cost = user_meals * meal_rate
        total_paid = paid_by_user.get(user_id, 0.0)
        balance = total_paid - meal_cost

        members.append({
            "user_id": user_id,
            "name": user.name if user else "Unknown",
            "total_meals": user_meals,
            "meal_cost": round(meal_cost, 2),
            "total_paid": round(total_paid, 2),
            "balance": round(balance, 2),
        })

    members.sort(key=lambda m: m["user_id"])

    return {
        "month": month,
        "total_expense": round(total_expense, 2),
        "total_meals": total_meals,
        "meal_rate": round(meal_rate, 2),
        "members": members,
    }