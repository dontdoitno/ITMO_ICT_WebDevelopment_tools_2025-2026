from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field


class NotificationTypeEnum(str, Enum):
    budget_exceeded = 'budget_exceeded'
    goal_reached = 'goal_reached'
    reminder = 'reminder'
    system = 'system'


class Notification(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    type: NotificationTypeEnum
    message: str
    is_read: bool = Field(default=False)
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(), server_default=func.now()
        )
    )
