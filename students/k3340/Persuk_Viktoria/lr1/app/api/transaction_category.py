'''
- [ ] POST /transactions/{id}/categories — assign category (update budget spent_amount)
- [ ] DELETE /transactions/{id}/categories/{category_id} — remove link (reverse budget spent_amount)
'''
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from auth.utils import get_current_user
from connector import get_session
from models.user import User
from models.budget import Budget, StatusType
from models.category import Category
from models.notification import Notification, NotificationTypeEnum
from models.transaction import Transaction
from models.transaction_category import TransactionCategory
from schemas.transaction_category import TransactionCategoryCreate, TransactionCategoryRead


router = APIRouter(
    prefix='/transactions',
    tags=['transaction-categories']
)

@router.post('/{id}/categories')
def assign_category_to_transaction(
    id: int,
    data: TransactionCategoryCreate,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> TransactionCategoryRead:

    transaction_db = session.exec(select(Transaction)
                                  .where(Transaction.id == id)
                                  .where(Transaction.user_id == current_user.id)).first()

    if not transaction_db:
        raise HTTPException(status_code=404, detail='Transaction is not found')

    category_db = session.exec(select(Category)
                               .where(Category.id == data.category_id)
                               .where(Category.user_id == current_user.id)).first()

    if not category_db:
        raise HTTPException(status_code=404, detail='Category is not found')

    # check if this transaction category link already exists
    transaction_category_link = session.exec(select(TransactionCategory)
                                             .where(TransactionCategory.transaction_id == transaction_db.id)
                                             .where(TransactionCategory.category_id == category_db.id)).first()

    if transaction_category_link:
        raise HTTPException(status_code=409, detail='Dublicate detected')

    if data.allocated_amount > transaction_db.amount:
        raise HTTPException(status_code=400, detail='Allocated amount can\'t be more than transaction amount')

    new_transaction_category = TransactionCategory(
        transaction_id=id,
        category_id=data.category_id,
        allocated_amount=data.allocated_amount
    )

    # Updating budget spent amount with exact same category id
    budgets_with_category = session.exec(select(Budget).where(Budget.category_id == data.category_id)).all()

    for budget in budgets_with_category:
        transaction_date = transaction_db.transaction_date
        if budget.period_start <= transaction_date <= budget.period_end:
            budget.spent_amount += data.allocated_amount

            # check if budget limit amount is ok or not
            if budget.spent_amount > budget.limit_amount:
                budget.status = StatusType.exceeded

                new_notification = Notification(
                    user_id = current_user.id,
                    type=NotificationTypeEnum.budget_exceeded,
                    message=f'Budget for {category_db.name} is exceeded!',
                )

                session.add(new_notification)

            session.add(budget)

    session.add(new_transaction_category)
    session.commit()
    session.refresh(new_transaction_category)

    return new_transaction_category


@router.delete('/{id}/categories/{category_id}')
def delete_category_from_transaction(
    id: int,
    category_id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):

    transaction_category_db = session.exec(select(TransactionCategory)
                                           .where(TransactionCategory.transaction_id == id)
                                           .where(TransactionCategory.category_id == category_id)).first()

    if not transaction_category_db:
        raise HTTPException(status_code=404, detail='Transaction or category is not found')

    transaction_db = session.exec(select(Transaction)
                                  .where(Transaction.id == id)
                                  .where(Transaction.user_id == current_user.id)).first()

    category_db = session.exec(select(Category)
                            .where(Category.id == category_id)
                            .where(Category.user_id == current_user.id)).first()

    # Updating budget spent amount with exact same category id
    budgets_with_category = session.exec(select(Budget).where(Budget.category_id == category_id)).all()

    # Reverse budget spent_amount
    for budget in budgets_with_category:
        transaction_date = transaction_db.transaction_date
        if budget.period_start <= transaction_date <= budget.period_end:
            budget.spent_amount -= transaction_category_db.allocated_amount

            if budget.spent_amount <= budget.limit_amount:
                budget.status = StatusType.active

            session.add(budget)


    session.delete(transaction_category_db)
    session.commit()

    return {'message': f'Category {category_db.name} deleted from transaction {transaction_db.id} and budget spent amount reverted'}
