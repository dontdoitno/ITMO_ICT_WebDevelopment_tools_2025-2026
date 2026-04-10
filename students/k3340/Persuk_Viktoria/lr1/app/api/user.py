from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from auth.utils import get_current_user, hash_password
from connector import get_session
from models.user import User
from schemas.user import TokenResponse, UserRead, UserCreate, UserLogin, UserUpdate


router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.get('/{id}')
def get_user_by_id(
    id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> UserRead:
    user_db = session.exec(select(User).where(User.id == id)).first()

    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    return user_db


@router.patch('/{id}')
def update_user_by_id(
    id: int,
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> UserRead:
    if current_user.id != id:
        raise HTTPException(status_code=403, detail='Forbidden!!!')

    if data.password is not None:
        current_user.password_hash = hash_password(data.password)

    if data.full_name is not None:
        current_user.full_name = data.full_name

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{id}', status_code=200)
def delete_user_by_id(
    id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):
    if current_user.id != id:
        raise HTTPException(status_code=403, detail='Forbidden!!!')

    session.delete(current_user)
    session.commit()

    return {'detail': 'user deleted'}
