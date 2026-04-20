from enum import Enum
from datetime import datetime
from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field


class OperationType(str, Enum):
    """Category operation type: income or expense"""
    income = 'income'
    expense = 'expense'


class Category(SQLModel, table=True):
    """Stores income and expense categories created by users

    Attributes:
        id: Unique category identifier
        user_id: Reference to the user who created the category
        name: Category name (e.g., 'Food', 'Transport')
        type: Category type - income or expense
        created_at: Category creation date
    """
    id: int | None = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key='user.id')
    name: str
    type: OperationType
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(), server_default=func.now()
        )
    )
