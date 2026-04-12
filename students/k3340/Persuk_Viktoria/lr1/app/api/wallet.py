from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from auth.utils import get_current_user
from connector import get_session
from models.user import User
from models.wallet import Wallet
from schemas.wallet import WalletCreate, WalletRead, WalletUpdate


router = APIRouter(
    prefix='/wallets',
    tags=['wallet'],
)


def _get_user_wallet(id: int, current_user: User, session) -> WalletRead:

    wallet = session.exec(select(Wallet).where(Wallet.id == id)).first()

    if not wallet:
        raise HTTPException(status_code=404, detail='Wallet not found')

    if wallet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail='Forbidden!!!!')

    return wallet


@router.post('/')
def create_wallet(
    wallet_data: WalletCreate,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session),
) -> WalletRead:

    wallet_db = Wallet(
        user_id=current_user.id,
        name=wallet_data.name,
        currency=wallet_data.currency,
        balance=wallet_data.balance
    )

    session.add(wallet_db)
    session.commit()
    session.refresh(wallet_db)

    return wallet_db


@router.get('/')
def list_wallets(
    current_user: User = Depends(get_current_user),
    session=Depends(get_session),
) -> List[WalletRead]:

    wallets = session.exec(select(Wallet).where(Wallet.user_id == current_user.id)).all()

    return wallets


@router.get('/{id}')
def get_wallet_by_id(
    id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session),
) -> WalletRead:

    wallet = _get_user_wallet(id, current_user, session)

    return wallet


@router.patch('/{id}')
def update_wallet_by_id(
    id: int,
    data: WalletUpdate,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> WalletRead:

    wallet = _get_user_wallet(id, current_user, session)

    if data.name is not None:
        wallet.name = data.name

    if data.currency is not None:
        wallet.currency = data.currency

    session.add(wallet)
    session.commit()
    session.refresh(wallet)


    return wallet


@router.delete('/{id}')
def delete_wallet_by_id(
    id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session),
):

    wallet = _get_user_wallet(id, current_user, session)

    session.delete(wallet)
    session.commit()

    return {'detail': 'wallet deleted'}
