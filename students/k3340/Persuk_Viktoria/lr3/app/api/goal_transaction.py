from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from auth.utils import get_current_user
from connector import get_session
from models.user import User
from models.budget import Budget, StatusType
from models.goal import Goal, GoalStatusType
from models.notification import Notification, NotificationTypeEnum
from models.transaction import Transaction
from models.goal_transaction import GoalTransaction
from schemas.goal_transaction import GoalTransactionRead, GoalTransactionCreate


router = APIRouter(
    prefix='/goals',
    tags=['goal-transactions']
)


@router.post('/{id}/transactions')
def link_transaction_to_goal(
    id: int,
    data: GoalTransactionCreate,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> GoalTransactionRead:

    goal_db = session.exec(select(Goal).where(Goal.id == id).where(Goal.user_id == current_user.id)).first()

    if not goal_db:
        raise HTTPException(status_code=404, detail='Goal is not found')

    transaction_db = session.exec(select(Transaction).where(Transaction.id == data.transaction_id).where(Transaction.user_id == current_user.id)).first()

    if not transaction_db:
        raise HTTPException(status_code=404, detail='Transaction is not found')

    goal_transaction_db = session.exec(select(GoalTransaction)
                                       .where(GoalTransaction.goal_id == id)
                                       .where(GoalTransaction.transaction_id == data.transaction_id)).first()

    if goal_transaction_db:
        raise HTTPException(status_code=409, detail='Duplicate detected')

    if data.allocated_amount > transaction_db.amount:
        raise HTTPException(status_code=400, detail='Allocated amount can\'t be more than transaction amount')

    new_goal_transaction = GoalTransaction(
        goal_id=id,
        transaction_id=data.transaction_id,
        allocated_amount=data.allocated_amount
    )

    goal_db.current_amount += data.allocated_amount
    if goal_db.current_amount >= goal_db.target_amount:
        goal_db.status = GoalStatusType.completed

        new_notification = Notification(
            user_id=current_user.id,
            type=NotificationTypeEnum.goal_reached,
            message=f'Congratulations! Your goal {goal_db.name.lower()} is reached!'
        )

        session.add(new_notification)

    session.add(new_goal_transaction)
    session.add(goal_db)
    session.commit()
    session.refresh(new_goal_transaction)

    return new_goal_transaction


@router.delete('/{id}/transactions/{transaction_id}')
def delete_transaction_from_goal(
    id: int,
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):

    goal_transaction_db = session.exec(select(GoalTransaction)
                                       .where(GoalTransaction.goal_id == id)
                                       .where(GoalTransaction.transaction_id == transaction_id)).first()

    if not goal_transaction_db:
        raise HTTPException(status_code=404, detail='Goal or transaction is not found')

    goal_db = session.exec(select(Goal).where(Goal.id == id).where(Goal.user_id == current_user.id)).first()

    transaction_db = session.exec(select(Transaction).where(Transaction.id == transaction_id).where(Transaction.user_id == current_user.id)).first()

    goal_db.current_amount -= goal_transaction_db.allocated_amount
    if (goal_db.status == GoalStatusType.completed) and (goal_db.current_amount < goal_db.target_amount):
        goal_db.status = GoalStatusType.active

    session.delete(goal_transaction_db)
    session.add(goal_db)
    session.commit()

    return {'message': f'Transaction {transaction_db.id} was successfully deleted from goal {goal_db.name.lower()}'}
