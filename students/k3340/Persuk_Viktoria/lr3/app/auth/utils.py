import jwt
import os

from datetime import datetime, timedelta
from dotenv import load_dotenv
from passlib.context import CryptContext
from typing import Annotated
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select

from models.user import User
from connector import get_session


load_dotenv()

pwd_context = CryptContext(schemes=['bcrypt'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

jwt_secret = os.getenv('JWT_SECRET')
jwt_algorithm = os.getenv('JWT_ALGORITHM')
jwt_expire_time = os.getenv('JWT_EXPIRE_MINUTES')

if not jwt_secret or not jwt_algorithm or not jwt_expire_time:
    raise ValueError('JWT config not set in .env file')


def hash_password(password: str) -> str:
    """Hash a password using bcrypt

    Args:
        password: Plain-text password

    Returns:
        Hashed password string
    """
    return pwd_context.hash(password[:72])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against its hash

    Args:
        plain_password: Plain-text password
        hashed_password: Hashed password from the database

    Returns:
        True if the password matches the hash, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Create a JWT access token

    Args:
        data: Payload data to encode in the token

    Returns:
        Encoded JWT token string
    """
    expire_time = datetime.now() + timedelta(minutes=int(jwt_expire_time))
    data['exp'] = expire_time
    return jwt.encode(data, jwt_secret, algorithm=jwt_algorithm)


def verify_token(token: str) -> dict:
    """Decode and verify a JWT token

    Args:
        token: JWT token to verify

    Returns:
        Decoded token payload

    Raises:
        HTTPException: 401 if the token is expired or invalid
    """
    try:
        return jwt.decode(token, jwt_secret, algorithms=[jwt_algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token is expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')


def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session=Depends(get_session)
    ) -> User:
    """Get the current user from the JWT token in the Authorization header

    Args:
        token: JWT token (extracted automatically via OAuth2)
        session: Database session (injected via Depends)

    Returns:
        User object from the database

    Raises:
        HTTPException: 401 if the token is invalid, 404 if the user is not found
    """
    user_data = verify_token(token)
    user_id = int(user_data['sub'])

    user_db = session.exec(select(User).where(User.id == user_id)).first()

    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    return user_db
