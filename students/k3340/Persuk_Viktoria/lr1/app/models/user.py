from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func


class User(SQLModel, table=True):
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
