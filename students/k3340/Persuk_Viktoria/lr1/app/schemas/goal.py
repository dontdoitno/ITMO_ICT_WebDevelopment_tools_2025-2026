from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

from models.goal import GoalStatusType


class GoalCreate(BaseModel):
    name: str
    target_amount: float
    deadline: date


class GoalRead(BaseModel):
    id: int
    user_id: int
    name: str
    target_amount: float
    current_amount: float
    deadline: date
    status: GoalStatusType
    created_at: datetime


class GoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    deadline: Optional[date] = None
    status: Optional[GoalStatusType] = None
