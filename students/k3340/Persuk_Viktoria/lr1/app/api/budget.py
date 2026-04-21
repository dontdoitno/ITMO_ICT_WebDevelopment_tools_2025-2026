'''
- [ ] POST /budgets — create budget (verify category belongs to user)
- [ ] GET /budgets — list user's budgets
- [ ] PATCH /budgets/{id} — update budget (verify ownership)
- [ ] DELETE /budgets/{id} — delete budget (verify ownership)
- [ ] GET /budgets/{id}/status — return budget with spent vs limit info
'''
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from auth.utils import get_current_user
from connector import get_session
from models.user import User
from models.budget import Budget
from models.category import Category
from schemas.budget import BudgetCreate, BudgetRead, BudgetUpdate


router = APIRouter(
    prefix='/budgets',
    tags=['budgets']
)


@router.post('/')
def create_budget(
    data: BudgetCreate,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> BudgetRead:

    user_category = session.exec(select(Category).where(data.category_id == Category.id).where(current_user.id == Category.user_id)).first()

    if not user_category:
        raise HTTPException(status_code=404, detail='Category is not found')

    new_budget = Budget(
        user_id=current_user.id,
        category_id=data.category_id,
        period_start=data.period_start,
        period_end=data.period_end,
        limit_amount=data.limit_amount
    )

    session.add(new_budget)
    session.commit()
    session.refresh(new_budget)

    return new_budget


@router.get('/')
def get_budgets(
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> List[BudgetRead]:

    budgets = session.exec(select(Budget).where(Budget.user_id == current_user.id)).all()

    return budgets


@router.patch('/{id}')
def update_budget(
    id: int,
    data: BudgetUpdate,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> BudgetRead:

    budget_db = session.exec(select(Budget).where(Budget.id == id).where(Budget.user_id == current_user.id)).first()

    if not budget_db:
        raise HTTPException(status_code=404, detail='Budget not found')

    if data.period_start is not None:
        budget_db.period_start = data.period_start
    if data.period_end is not None:
        budget_db.period_end = data.period_end
    if data.limit_amount is not None:
        budget_db.limit_amount = data.limit_amount
    if data.status is not None:
        budget_db.status = data.status

    session.add(budget_db)
    session.commit()
    session.refresh(budget_db)

    return budget_db


@router.delete('/{id}')
def delete_budget(
    id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):

    budget_db = session.exec(select(Budget).where(Budget.id == id).where(Budget.user_id == current_user.id)).first()

    if not budget_db:
        raise HTTPException(status_code=404, detail='Budget not found')

    session.delete(budget_db)
    session.commit()

    return {'message': 'budget deleted'}


@router.get('/{id}/status')
def get_budget_info(
    id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):

    budget_db = session.exec(select(Budget).where(Budget.id == id).where(Budget.user_id == current_user.id)).first()

    if not budget_db:
        raise HTTPException(status_code=404, detail='Budget not found')

    remained = budget_db.limit_amount - budget_db.spent_amount
    percentage = round((budget_db.spent_amount / budget_db.limit_amount) * 100, 2) if budget_db.limit_amount > 0 else 0

    message = {
        'Budget limit': budget_db.limit_amount,
        'Spent so far': budget_db.spent_amount,
        'Remaining': remained,
        'Percentage used': f'{percentage}%',
        'Status': budget_db.status
    }

    return message
