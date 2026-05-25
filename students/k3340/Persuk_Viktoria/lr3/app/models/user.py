from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func


class User(SQLModel, table=True):
    """Database model representing a user

    Attributes:
        id: Unique user identifier (primary key)
        email: User email address (unique field)
        full_name: Full name of the user
        password_hash: Bcrypt-hashed password
        created_at: Timestamp of record creation (auto-filled)
        updated_at: Timestamp of last record update (auto-updated)
    """
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    full_name: str
    password_hash: str
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(), server_default=func.now()
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(), server_default=func.now(), onupdate=func.now()
        )
    )
