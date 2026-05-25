from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class CurrencyType(str, Enum):
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'


class WalletCreate(BaseModel):
    """Schema for creating a new wallet

    Attributes:
        name: Display name of the wallet
        currency: Currency code of the wallet
        balance: Initial balance (defaults to 0)
    """
    name: str
    currency: CurrencyType
    balance: Optional[float] = 0


class WalletRead(BaseModel):
    """Schema for wallet response data

    Attributes:
        id: Unique wallet identifier
        name: Display name of the wallet
        currency: Currency code of the wallet
        balance: Current wallet balance
        created_at: Wallet creation timestamp
        updated_at: Last wallet update timestamp
    """
    id: int
    name: str
    currency: CurrencyType
    balance: float
    created_at: datetime
    updated_at: datetime


class WalletUpdate(BaseModel):
    """Schema for partial wallet update

    All fields are optional — only changed fields need to be provided

    Attributes:
        name: New display name of the wallet
        currency: New currency code of the wallet
    """
    name: Optional[str] = None
    currency: Optional[CurrencyType] = None
