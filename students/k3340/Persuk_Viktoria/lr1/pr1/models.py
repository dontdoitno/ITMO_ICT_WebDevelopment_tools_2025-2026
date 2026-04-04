from pydantic import BaseModel
from enum import Enum


class CurrencyType(str, Enum):
    '''
    ENUM для валют счёта
    '''
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'
    CNY = 'CNY'


class User(BaseModel):
    id: int
    email: str
    password_hash: str
    first_name: str
    middle_name: str | None = None
    last_name: str
    # TODO: make it datetime
    created_at: str
    updated_at: str


class Account(BaseModel):
    id: int
    user: User
    name: str
    currency: CurrencyType
    balance: float
    # TODO: make it datetime
    created_at: str


class AccountResponse(BaseModel):
    status: str
    data: Account | None = None
    message: str | None = None
