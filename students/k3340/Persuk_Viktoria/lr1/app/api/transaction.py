'''
- [ ] POST /transactions — create transaction + update wallet balance
- [ ] GET /transactions — list user's transactions (with filters: type, wallet_id, date range)
- [ ] GET /transactions/{id} — get transaction (verify ownership)
- [ ] PATCH /transactions/{id} — update transaction + adjust balance if amount/type changed
- [ ] DELETE /transactions/{id} — delete transaction + reverse balance change
'''

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from api.wallet import _get_user_wallet
from auth.utils import get_current_user
from connector import get_session
from models.user import User
from models.transaction import Transaction, TransactionType
from schemas.transaction import TransactionRead, TransactionCreate, TransactionUpdate


router = APIRouter(
    prefix='/transactions',
    tags=['transactions']
)


@router.get('/')
def list_transactions(
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> List[TransactionRead]:

    transctions = session.exec(select(Transaction).where(Transaction.user_id == current_user.id)).all()

    return transctions


@router.get('/{id}')
def get_transaction_by_id(
    id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> TransactionRead:

    transaction = session.exec(select(Transaction).where(Transaction.id == id).where(Transaction.user_id == current_user.id)).first()

    if not transaction:
        raise HTTPException(status_code=404, detail='Transaction is not found')

    return transaction


@router.post('/')
def create_transaction(
    data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> TransactionRead:

    wallet = _get_user_wallet(
        id=data.wallet_id,
        current_user=current_user,
        session=session
    )

    new_transaction = Transaction(
        user_id=current_user.id,
        wallet_id=wallet.id,
        type=data.type,
        amount=data.amount,
        description=data.description,
        transaction_date=data.transaction_date
    )

    # change amount in wallet
    if data.type == TransactionType.expense:
        wallet.balance -= data.amount
    elif data.type == TransactionType.income:
        wallet.balance += data.amount

    session.add(new_transaction)
    session.add(wallet)
    session.commit()
    session.refresh(new_transaction)

    return new_transaction


@router.patch('/{id}')
def update_transaction(
    id: int,
    data: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> TransactionRead:

    transaction_db = session.exec(select(Transaction).where(Transaction.id == id).where(Transaction.user_id == current_user.id)).first()

    if not transaction_db:
        raise HTTPException(status_code=404, detail='Transaction is not found')

    wallet = _get_user_wallet(
        id=transaction_db.wallet_id,
        current_user=current_user,
        session=session
    )


    current_balance = wallet.balance
    current_amount = transaction_db.amount

    # Reverse old transaction effect
    if transaction_db.type == TransactionType.income:
        wallet.balance -= transaction_db.amount
    else:
        wallet.balance += transaction_db.amount

    # Update fields
    if data.type is not None:
        transaction_db.type = data.type
    if data.amount is not None:
        transaction_db.amount = data.amount
    if data.description is not None:
        transaction_db.description = data.description
    if data.transaction_date is not None:
        transaction_db.transaction_date = data.transaction_date

    # Apply new transaction effect
    if transaction_db.type == TransactionType.income:
        wallet.balance += transaction_db.amount
    else:
        wallet.balance -= transaction_db.amount

    session.add(wallet)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)

    return transaction_db


@router.delete('/{id}')
def delete_transaction(
    id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):

    transaction_db = session.exec(select(Transaction).where(Transaction.id == id)).first()

    if not transaction_db:
        raise HTTPException(status_code=404, detail='Transaction not found')

    wallet = _get_user_wallet(
        id=transaction_db.wallet_id,
        current_user=current_user,
        session=session
    )

    if transaction_db.type == TransactionType.income:
        wallet.balance -= transaction_db.amount
    elif transaction_db.type == TransactionType.expense:
        wallet.balance += transaction_db.amount

    session.add(wallet)
    session.delete(transaction_db)
    session.commit()

    return {'message': 'transaction deleted'}
