from enum import Enum
from datetime import date, datetime
from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field


class StatusType(str, Enum):
    """Budget status tracking"""
    active = 'active'
    exceeded = 'exceeded'
    closed = 'closed'


class Budget(SQLModel, table=True):
    """Stores user budgets by category with spending limits and period tracking

    Attributes:
        id: Unique budget identifier
        user_id: Reference to the user
        category_id: Category for which the budget is set
        period_start: Budget period start date
        period_end: Budget period end date
        limit_amount: Maximum allowed spending
        spent_amount: Actual spent amount
        status: Budget status - active, exceeded, or closed
        created_at: Budget creation date
    """
    id: int | None = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key='user.id')
    category_id: int = Field(foreign_key='category.id')
    period_start: date
    period_end: date
    limit_amount: float = Field(gt=0)
    spent_amount: float = Field(default=0)
    status: StatusType = Field(default=StatusType.active)
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(), server_default=func.now()
        )
    )
