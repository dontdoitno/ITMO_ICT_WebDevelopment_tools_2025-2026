from pydantic import BaseModel


class TransactionCategoryCreate(BaseModel):
    category_id: int
    allocated_amount: float


class TransactionCategoryRead(BaseModel):
    transaction_id: int
    category_id: int
    allocated_amount: float
