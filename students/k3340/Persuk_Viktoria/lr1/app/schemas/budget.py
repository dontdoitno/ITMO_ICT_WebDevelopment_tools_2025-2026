from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

from models.budget import StatusType


class BudgetCreate(BaseModel):
    """Schema for creating a new budget for a category

    Attributes:
        category_id: ID of the category to budget
        period_start: Budget period start date
        period_end: Budget period end date
        limit_amount: Maximum allowed spending
    """
    category_id: int
    period_start: date
    period_end: date
    limit_amount: float


class BudgetRead(BaseModel):
    """Schema for budget response data with spending info

    Attributes:
        id: Unique budget identifier
        user_id: Owner user ID
        category_id: Budgeted category ID
        period_start: Budget period start date
        period_end: Budget period end date
        limit_amount: Maximum allowed spending
        spent_amount: Actual spent amount
        status: Budget status - active, exceeded, or closed
        created_at: Budget creation timestamp
    """
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
    """Schema for updating budget fields (all optional)

    Attributes:
        period_start: New period start date
        period_end: New period end date
        limit_amount: New spending limit
        status: New budget status
    """
    period_start: Optional[date] = None
    period_end: Optional[date] = None
    limit_amount: Optional[float] = None
    status: Optional[StatusType] = None
