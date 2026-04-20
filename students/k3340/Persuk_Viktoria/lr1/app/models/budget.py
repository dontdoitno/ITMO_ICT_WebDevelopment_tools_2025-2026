from enum import Enum
from datetime import date, datetime
from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field


class StatusType(str, Enum):
    active = 'active'
    exceeded = 'exceeded'
    closed = 'closed'


class Budget(SQLModel, table=True):
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
