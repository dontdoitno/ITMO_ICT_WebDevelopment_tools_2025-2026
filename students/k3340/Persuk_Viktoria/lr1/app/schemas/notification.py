from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from models.notification import NotificationTypeEnum


class NotificationRead(BaseModel):
    """Schema for notification response data

    Attributes:
        id: Unique notification identifier
        user_id: Owner user ID
        type: Notification type
        message: Notification message text
        is_read: Whether the notification has been read
        created_at: Notification creation timestamp
    """
    id: int
    user_id: int
    type: NotificationTypeEnum
    message: str
    is_read: bool
    created_at: datetime


class NotificationUpdate(BaseModel):
    """Schema for updating notification read status

    Attributes:
        is_read: New read status
    """
    is_read: Optional[bool] = None
