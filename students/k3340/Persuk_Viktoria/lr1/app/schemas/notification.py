from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from models.notification import NotificationTypeEnum


class NotificationRead(BaseModel):
    id: int
    user_id: int
    type: NotificationTypeEnum
    message: str
    is_read: bool
    created_at: datetime


class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None
