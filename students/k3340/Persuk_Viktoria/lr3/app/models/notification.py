from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field


class NotificationTypeEnum(str, Enum):
    """Types of user notifications"""
    budget_exceeded = 'budget_exceeded'
    goal_reached = 'goal_reached'
    reminder = 'reminder'
    system = 'system'


class Notification(SQLModel, table=True):
    """Stores user notifications about financial events

    Attributes:
        id: Unique notification identifier
        user_id: Reference to the user
        type: Notification type (budget_exceeded, goal_reached, reminder, system)
        message: Notification message text
        is_read: Whether the notification has been read
        created_at: Notification creation timestamp
    """
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
