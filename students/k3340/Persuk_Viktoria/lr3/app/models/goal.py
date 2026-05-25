from enum import Enum
from datetime import datetime, date
from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field


class GoalStatusType(str, Enum):
    """Financial goal status tracking"""
    active = 'active'
    completed = 'completed'
    cancelled = 'cancelled'


class Goal(SQLModel, table=True):
    """Stores user financial goals with target amounts and deadlines

    Attributes:
        id: Unique goal identifier
        user_id: Reference to the user
        name: Goal name (e.g., 'Buy a laptop')
        target_amount: Target amount to reach
        current_amount: Current progress toward the goal
        deadline: Target completion date
        status: Goal status - active, completed, or cancelled
        created_at: Goal creation date
    """
    id: int | None = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key='user.id')
    name: str
    target_amount: float = Field(gt=0)
    current_amount: float = Field(default=0)
    deadline: date
    status: GoalStatusType = Field(default=GoalStatusType.active)
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(), server_default=func.now()
        )
    )
