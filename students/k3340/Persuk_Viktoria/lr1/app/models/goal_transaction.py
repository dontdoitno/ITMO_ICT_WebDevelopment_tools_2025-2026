from sqlmodel import SQLModel, Field


class GoalTransaction(SQLModel, table=True):
    goal_id: int | None = Field(default=None, foreign_key='goal.id', primary_key=True)
    transaction_id: int | None = Field(default=None, foreign_key='transaction.id', primary_key=True)
    allocated_amount: float = Field(gt=0)
