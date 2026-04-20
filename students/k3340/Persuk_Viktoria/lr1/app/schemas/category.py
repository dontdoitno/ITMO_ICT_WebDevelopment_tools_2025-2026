from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from models.category import OperationType


class CategoryCreate(BaseModel):
    """Schema for creating a new category

    Attributes:
        name: Category name
        type: Category type - income or expense
    """
    name: str
    type: OperationType


class CategoryRead(BaseModel):
    """Schema for category response data

    Attributes:
        id: Unique category identifier
        user_id: Owner user ID
        name: Category name
        type: Category type - income or expense
        created_at: Category creation timestamp
    """
    id: int
    user_id: int
    name: str
    type: OperationType
    created_at: datetime


class CategoryUpdate(BaseModel):
    """Schema for updating category fields (all optional)

    Attributes:
        name: New category name
        type: New category type
    """
    name: Optional[str] = None
    type: Optional[OperationType] = None
