from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class TransactionBase(BaseModel):
    """Base schema with common transaction fields

    Attributes:
        type: Transaction type (income or expense)
        amount: Transaction amount
        description: Text description of the transaction
        transaction_date: Date when the transaction occurred
    """
    type: str
    amount: float
    description: str
    transaction_date: date


class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction

    Attributes:
        wallet_id: ID of the wallet to associate the transaction with
    """
    wallet_id: int


class TransactionRead(TransactionBase):
    """Schema for transaction response data

    Attributes:
        id: Unique transaction identifier
        wallet_id: ID of the associated wallet
        user_id: ID of the transaction owner
        created_at: Transaction creation timestamp
    """
    id: int
    wallet_id: int
    user_id: int
    created_at: datetime


class TransactionUpdate(BaseModel):
    """Schema for partial transaction update

    All fields are optional — only changed fields need to be provided

    Attributes:
        type: New transaction type (income or expense)
        amount: New transaction amount
        description: New text description
        transaction_date: New transaction date
    """
    type: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    transaction_date: Optional[date] = None
