from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


# ---------- User ----------

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    created_at: datetime


# ---------- Meal ----------

class MealCreate(BaseModel):
    user_id: int
    date: date
    meal_count: int = Field(ge=0, le=3, description="0-3 meals per day")


class MealOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    date: date
    meal_count: int
    created_at: datetime


# ---------- Expense ----------

class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)
    description: str | None = Field(default=None, max_length=255)
    date: date
    paid_by_user_id: int


class ExpenseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: float
    description: str | None
    date: date
    paid_by_user_id: int
    created_at: datetime


# ---------- Deposit ----------

class DepositCreate(BaseModel):
    user_id: int
    amount: float = Field(gt=0)
    date: date


class DepositOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    amount: float
    date: date
    created_at: datetime


# ---------- Settlement ----------

class MemberSettlement(BaseModel):
    user_id: int
    name: str
    total_meals: int
    meal_cost: float
    total_paid: float
    balance: float


class SettlementOut(BaseModel):
    month: str
    total_expense: float
    total_meals: int
    meal_rate: float
    members: list[MemberSettlement]

