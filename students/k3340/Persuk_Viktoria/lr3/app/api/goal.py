from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from auth.utils import get_current_user
from connector import get_session
from models.user import User
from models.goal import Goal
from schemas.goal import GoalCreate, GoalRead, GoalUpdate


router = APIRouter(
    prefix='/goals',
    tags=['goals']
)


@router.post('/')
def create_goal(
    data: GoalCreate,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> GoalRead:

    new_goal = Goal(
        user_id=current_user.id,
        name=data.name,
        target_amount=data.target_amount,
        deadline=data.deadline
    )

    session.add(new_goal)
    session.commit()
    session.refresh(new_goal)

    return new_goal


@router.get('/')
def get_goals(
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> List[GoalRead]:

    goals = session.exec(select(Goal).where(Goal.user_id == current_user.id)).all()

    return goals


@router.patch('/{id}')
def update_goal(
    id: int,
    data: GoalUpdate,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> GoalRead:

    goal_db = session.exec(select(Goal).where(Goal.id == id).where(Goal.user_id == current_user.id)).first()

    if not goal_db:
        raise HTTPException(status_code=404, detail='Goal is not found')

    if data.name is not None:
        goal_db.name = data.name
    if data.target_amount is not None:
        goal_db.target_amount = data.target_amount
    if data.deadline is not None:
        goal_db.deadline = data.deadline
    if data.status is not None:
        goal_db.status = data.status

    session.add(goal_db)
    session.commit()
    session.refresh(goal_db)

    return goal_db


@router.delete('/{id}')
def delete_goal(
    id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):

    goal_db = session.exec(select(Goal).where(Goal.id == id).where(Goal.user_id == current_user.id)).first()

    if not goal_db:
        raise HTTPException(status_code=404, detail='Goal is not found')

    session.delete(goal_db)
    session.commit()

    return {'message': 'goal deteled'}
