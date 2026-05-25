from sqlmodel import SQLModel, Field


class GoalTransaction(SQLModel, table=True):
    """Associative table linking goals to transactions (many-to-many)

    Attributes:
        goal_id: Reference to the financial goal
        transaction_id: Reference to the transaction
        allocated_amount: Amount from the transaction allocated toward the goal
    """
    goal_id: int | None = Field(default=None, foreign_key='goal.id', primary_key=True)
    transaction_id: int | None = Field(default=None, foreign_key='transaction.id', primary_key=True)
    allocated_amount: float = Field(gt=0)
