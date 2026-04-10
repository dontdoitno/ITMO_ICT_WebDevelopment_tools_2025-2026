from datetime import datetime, date
from enum import Enum
from typing import Optional
from sqlalchemy import Column, DateTime, Date, func
from sqlmodel import SQLModel, Field


class TransactionType(str, Enum):
    income = 'income'
    expense = 'expense'


class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    wallet_id: int = Field(foreign_key='wallet.id')
    type: TransactionType
    amount: float = Field(gt=0)
    description: Optional[str] = None
    transaction_date: date = Field(
        sa_column=Column(
            Date, server_default=func.current_date()
        )
    )
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(), server_default=func.now()
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(), server_default=func.now(), onupdate=func.now()
        )
    )
