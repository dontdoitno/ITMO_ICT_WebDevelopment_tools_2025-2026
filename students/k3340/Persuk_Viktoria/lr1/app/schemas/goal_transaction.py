from pydantic import BaseModel


class GoalTransactionCreate(BaseModel):
    """Schema for linking a transaction to a goal

    Attributes:
        transaction_id: ID of the transaction to link
        allocated_amount: Amount from transaction allocated toward the goal
    """
    transaction_id: int
    allocated_amount: float


class GoalTransactionRead(BaseModel):
    """Schema for goal-transaction link response data

    Attributes:
        goal_id: Linked goal ID
        transaction_id: Linked transaction ID
        allocated_amount: Amount allocated toward the goal
    """
    goal_id: int
    transaction_id: int
    allocated_amount: float
