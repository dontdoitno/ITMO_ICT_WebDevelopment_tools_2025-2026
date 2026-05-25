import os

from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel


load_dotenv()

db_url = os.getenv('DB_ADMIN')
if not db_url:
    raise ValueError('DB_ADMIN is not set')

engine = create_engine(db_url, echo=True)


def init_db():
    """Create all database tables on startup."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """DB session generator."""
    with Session(engine) as session:
        yield session
