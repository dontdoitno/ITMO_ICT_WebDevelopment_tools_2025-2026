from datetime import datetime, date
from enum import Enum
from typing import Optional
from sqlalchemy import Column, DateTime, Date, func
from sqlmodel import SQLModel, Field


class TransactionType(str, Enum):
    """Enum representing the type of a financial transaction (income / expense)"""
    income = 'income'
    expense = 'expense'


class Transaction(SQLModel, table=True):
    """Database model representing a financial transaction

    Attributes:
        id: Unique transaction identifier (primary key)
        user_id: Foreign key referencing the transaction owner
        wallet_id: Foreign key referencing the associated wallet
        type: Transaction type (income or expense)
        amount: Transaction amount (must be greater than 0)
        description: Optional text description of the transaction
        transaction_date: Date when the transaction occurred (defaults to current date)
        created_at: Timestamp of record creation (auto-filled)
        updated_at: Timestamp of last record update (auto-updated)
    """
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    wallet_id: int = Field(foreign_key='wallet.id')
    type: TransactionType
    amount: float = Field(default=0.0)
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
