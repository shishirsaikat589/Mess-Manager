from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import extract
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.utils import parse_month

router = APIRouter(prefix="/meals", tags=["meals"])


@router.post("", response_model=schemas.MealOut, status_code=status.HTTP_201_CREATED)
def create_meal(payload: schemas.MealCreate, db: Session = Depends(get_db)):
    user = db.get(models.User, payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    meal = models.MealEntry(
        user_id=payload.user_id,
        date=payload.date,
        meal_count=payload.meal_count,
    )
    db.add(meal)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="This user already has a meal entry for that date",
        )
    db.refresh(meal)
    return meal


@router.get("", response_model=list[schemas.MealOut])
def list_meals(
    user_id: int | None = Query(default=None),
    month: str | None = Query(default=None, description="Format: YYYY-MM"),
    db: Session = Depends(get_db),
):
    query = db.query(models.MealEntry)

    if user_id is not None:
        query = query.filter(models.MealEntry.user_id == user_id)

    if month is not None:
        year, mon = parse_month(month)
        query = query.filter(
            extract("year", models.MealEntry.date) == year,
            extract("month", models.MealEntry.date) == mon,
        )

    return query.order_by(models.MealEntry.date).all()
