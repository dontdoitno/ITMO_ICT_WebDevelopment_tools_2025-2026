from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from models.category import OperationType


class CategoryCreate(BaseModel):
    name: str
    type: OperationType


class CategoryRead(BaseModel):
    id: int
    user_id: int
    name: str
    type: OperationType
    created_at: datetime


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[OperationType] = None
