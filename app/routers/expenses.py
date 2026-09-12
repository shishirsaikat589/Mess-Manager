from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import extract
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.utils import parse_month

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("", response_model=schemas.ExpenseOut, status_code=status.HTTP_201_CREATED)
def create_expense(payload: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    payer = db.get(models.User, payload.paid_by_user_id)
    if not payer:
        raise HTTPException(status_code=404, detail="paid_by_user_id does not match any user")

    expense = models.Expense(
        amount=payload.amount,
        description=payload.description,
        date=payload.date,
        paid_by_user_id=payload.paid_by_user_id,
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("", response_model=list[schemas.ExpenseOut])
def list_expenses(
    month: str | None = Query(default=None, description="Format: YYYY-MM"),
    paid_by: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Expense)

    if paid_by is not None:
        query = query.filter(models.Expense.paid_by_user_id == paid_by)

    if month is not None:
        year, mon = parse_month(month)
        query = query.filter(
            extract("year", models.MealEntry.date) == year,
            extract("month", models.MealEntry.date) == mon,
        )

    return query.order_by(models.Expense.date).all()