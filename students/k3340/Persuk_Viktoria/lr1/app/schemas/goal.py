from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

from models.goal import GoalStatusType


class GoalCreate(BaseModel):
    """Schema for creating a new financial goal

    Attributes:
        name: Goal name (e.g., 'Buy a laptop')
        target_amount: Target amount to save
        deadline: Target completion date
    """
    name: str
    target_amount: float
    deadline: date


class GoalRead(BaseModel):
    """Schema for goal response data with progress info

    Attributes:
        id: Unique goal identifier
        user_id: Owner user ID
        name: Goal name
        target_amount: Target amount to save
        current_amount: Current progress
        deadline: Target completion date
        status: Goal status - active, completed, or cancelled
        created_at: Goal creation timestamp
    """
    id: int
    user_id: int
    name: str
    target_amount: float
    current_amount: float
    deadline: date
    status: GoalStatusType
    created_at: datetime


class GoalUpdate(BaseModel):
    """Schema for updating goal fields (all optional)

    Attributes:
        name: New goal name
        target_amount: New target amount
        deadline: New deadline
        status: New goal status
    """
    name: Optional[str] = None
    target_amount: Optional[float] = None
    deadline: Optional[date] = None
    status: Optional[GoalStatusType] = None
