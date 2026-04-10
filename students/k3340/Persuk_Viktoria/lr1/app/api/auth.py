from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select

from models.user import User
from auth.utils import hash_password, verify_password, create_access_token, verify_token, get_current_user
from schemas.user import TokenResponse, UserRead, UserCreate, UserLogin, UserUpdate
from connector import get_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/register')
def register_user(
    user_data: UserCreate,
    session=Depends(get_session)
) -> UserRead:
    """Register a new user

    Args:
        user_data: Registration data (email, password, full_name)
        session: Database session

    Returns:
        Created user data (without password)

    Raises:
        HTTPException: 409 if the email is already registered
    """

    existing = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing:
        raise HTTPException(status_code=409, detail='This email is already registred')

    hashed_password = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        password_hash=hashed_password,
        full_name=user_data.full_name
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.post('/login')
def login_user(
    user_data: OAuth2PasswordRequestForm = Depends(),
    session=Depends(get_session)
) -> TokenResponse:
    """Authenticate a user and return a JWT token

    Args:
        user_data: Login credentials (email, password)
        session: Database session

    Returns:
        JWT access token
    """
    user_db = session.exec(select(User).where(User.email == user_data.username)).first()
    if not user_db:
        raise HTTPException(status_code=401, detail='Password or email is incorrect')

    curr_password = user_data.password
    hashed_password = user_db.password_hash

    if verify_password(curr_password, hashed_password):
        token = create_access_token({'sub': str(user_db.id)})
        return TokenResponse(
            access_token=token,
            token_type='bearer'
        )
    else:
        raise HTTPException(status_code=401, detail='Password or email is incorrect')


@router.get('/me')
def get_me(
    current_user: User = Depends(get_current_user)
) -> UserRead:
    """Return the currently authenticated user's data

    Args:
        current_user: Current user (extracted from JWT token)

    Returns:
        User data (without password)
    """
    return current_user
