from pydantic import BaseModel


class GoalTransactionCreate(BaseModel):
    transaction_id: int
    allocated_amount: float


class GoalTransactionRead(BaseModel):
    goal_id: int
    transaction_id: int
    allocated_amount: float
