from pydantic import BaseModel


class TransactionCategoryCreate(BaseModel):
    """Schema for assigning a category to a transaction

    Attributes:
        category_id: ID of the category to assign
        allocated_amount: Portion of transaction amount for this category
    """
    category_id: int
    allocated_amount: float


class TransactionCategoryRead(BaseModel):
    """Schema for transaction-category link response data

    Attributes:
        transaction_id: Linked transaction ID
        category_id: Linked category ID
        allocated_amount: Amount allocated to this category
    """
    transaction_id: int
    category_id: int
    allocated_amount: float
