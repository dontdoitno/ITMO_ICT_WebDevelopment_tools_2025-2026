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
    """Get a user by their ID

    Args:
        id: User ID to look up
        current_user: Authenticated user (extracted from JWT token)
        session: Database session

    Returns:
        User data (without password)

    Raises:
        HTTPException: 404 if the user is not found
    """
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
    """Update a user's data by their ID

    Args:
        id: User ID to update
        data: Fields to update (password and/or full_name)
        current_user: Authenticated user (extracted from JWT token)
        session: Database session

    Returns:
        Updated user data (without password)

    Raises:
        HTTPException: 403 if the user tries to update another user's data
    """
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
    """Delete a user by their ID

    Args:
        id: User ID to delete
        current_user: Authenticated user (extracted from JWT token)
        session: Database session

    Returns:
        Confirmation message

    Raises:
        HTTPException: 403 if the user tries to delete another user's account
    """
    if current_user.id != id:
        raise HTTPException(status_code=403, detail='Forbidden!!!')

    session.delete(current_user)
    session.commit()

    return {'detail': 'user deleted'}
