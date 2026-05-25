from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for registering a new user

    Attributes:
        email: User email address
        password: Plain-text password (will be hashed before saving)
        full_name: Full name of the user
    """
    email: str
    password: str
    full_name: str


class UserLogin(BaseModel):
    """Schema for user authentication

    Attributes:
        email: User email address
        password: Plain-text password for verification
    """
    email: str
    password: str


class UserRead(BaseModel):
    """Schema for user response data (excludes password)

    Attributes:
        id: Unique user identifier
        email: User email address
        full_name: Full name of the user
        created_at: Account creation timestamp
        updated_at: Last account update timestamp
    """
    id: int
    email: str
    full_name: str
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    """Schema for partial user update

    All fields are optional — only changed fields need to be provided

    Attributes:
        password: New password (will be hashed before saving)
        full_name: New full name of the user
    """
    password: Optional[str] = None
    full_name: Optional[str] = None


class TokenResponse(BaseModel):
    """Schema for successful authentication response

    Attributes:
        access_token: JWT access token
        token_type: Token type (e.g. 'bearer')
    """
    access_token: str
    token_type: str
