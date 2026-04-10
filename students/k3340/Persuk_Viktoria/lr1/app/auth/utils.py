import jwt
import os

from datetime import datetime, timedelta
from dotenv import load_dotenv
from passlib.context import CryptContext
from typing import Annotated
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select

from app.models.user import User
from connector import get_session


load_dotenv()

pwd_context = CryptContext(schemes=['bcrypt'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

jwt_secret = os.getenv('JWT_SECRET')
jwt_algorithm = os.getenv('JWT_ALGORITHM')
jwt_expire_time = os.getenv('JWT_EXPIRE_MINUTES')

if not jwt_secret or not jwt_algorithm or not jwt_expire_time:
    raise ValueError('JWT config not set in .env file')


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    expire_time = datetime.now() + timedelta(minutes=int(jwt_expire_time))
    data['exp'] = expire_time
    return jwt.encode(data, jwt_secret, jwt_algorithm)


def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, jwt_secret, jwt_algorithm)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token is expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')


def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session=Depends(get_session)
    ) -> User:
    user_data = verify_token(token)
    user_id = user_data['sub']

    user_db = session.exec(select(User).where(User.id == user_id)).first()

    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    return user_db
