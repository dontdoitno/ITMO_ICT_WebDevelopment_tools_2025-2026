from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field


class Wallet(SQLModel, table=True):
    """Database model representing a user's wallet

    Attributes:
        id: Unique wallet identifier (primary key)
        user_id: Foreign key referencing the wallet owner
        name: Display name of the wallet
        currency: Currency code of the wallet
        balance: Current wallet balance (defaults to 0)
        created_at: Timestamp of record creation (auto-filled)
        updated_at: Timestamp of last record update (auto-updated)
    """
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    name: str
    currency: str
    balance: float = Field(default=0)
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
