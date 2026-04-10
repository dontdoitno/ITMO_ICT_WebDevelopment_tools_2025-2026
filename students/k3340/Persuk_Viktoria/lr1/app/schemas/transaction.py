from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class TransactionBase(BaseModel):
    type: str
    amount: float
    description: str
    transaction_date: date


class TransactionCreate(TransactionBase):
    wallet_id: int


class TransactionRead(TransactionBase):
    id: int
    wallet_id: int
    user_id: int
    created_at: datetime


class TransactionUpdate(BaseModel):
    type: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    transaction_date: Optional[date] = None
