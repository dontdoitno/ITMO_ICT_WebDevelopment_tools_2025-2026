from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CategoryCreate(BaseModel):
    """Schema for creating a new category

    Attributes:
        name: Category name
    """
    name: str


class CategoryRead(BaseModel):
    """Schema for category response data

    Attributes:
        id: Unique category identifier
        user_id: Owner user ID
        name: Category name
        created_at: Category creation timestamp
    """
    id: int
    user_id: int
    name: str
    created_at: datetime


class CategoryUpdate(BaseModel):
    """Schema for updating category fields (all optional)

    Attributes:
        name: New category name
    """
    name: Optional[str] = None
