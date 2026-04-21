from sqlmodel import SQLModel, Field


class TransactionCategory(SQLModel, table=True):
    transaction_id: int | None = Field(default=None, foreign_key='transaction.id', primary_key=True)
    category_id: int | None = Field(default=None, foreign_key='category.id', primary_key=True)
    allocated_amount: float = Field(gt=0)
