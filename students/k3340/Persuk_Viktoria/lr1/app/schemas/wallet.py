from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WalletCreate(BaseModel):
    name: str
    currency: str
    balance: Optional[float] = 0


class WalletRead(BaseModel):
    id: int
    name: str
    currency: str
    balance: float
    created_at: datetime
    updated_at: datetime


class WalletUpdate(BaseModel):
    name: Optional[str] = None
    currency: Optional[str] = None
