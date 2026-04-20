from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

from models.budget import StatusType


class BudgetCreate(BaseModel):
    category_id: int
    period_start: date
    period_end: date
    limit_amount: float


class BudgetRead(BaseModel):
    id: int
    user_id: int
    category_id: int
    period_start: date
    period_end: date
    limit_amount: float
    spent_amount: float
    status: StatusType
    created_at: datetime


class BudgetUpdate(BaseModel):
    period_start: Optional[date] = None
    period_end: Optional[date] = None
    limit_amount: Optional[float] = None
    status: Optional[StatusType] = None
