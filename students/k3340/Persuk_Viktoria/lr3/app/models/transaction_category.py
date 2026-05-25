from sqlmodel import SQLModel, Field


class TransactionCategory(SQLModel, table=True):
    """Associative table linking transactions to categories (many-to-many)

    Attributes:
        transaction_id: Reference to the transaction
        category_id: Reference to the category
        allocated_amount: Portion of transaction amount assigned to this category
    """
    transaction_id: int | None = Field(default=None, foreign_key='transaction.id', primary_key=True)
    category_id: int | None = Field(default=None, foreign_key='category.id', primary_key=True)
    allocated_amount: float = Field(gt=0)
