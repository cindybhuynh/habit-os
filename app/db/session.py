from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings  # assumes you have settings.DATABASE_URL

# Create the DB engine (connection pool)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,   # drops dead connections automatically
    future=True,
)

# Session factory (use this to create new sessions)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    future=True,
)

def get_db():
    """
    FastAPI-style dependency (or just a generator you can use elsewhere).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # always closes, even if request crashes 

@contextmanager
def db_session():
    """
    Convenient context manager for scripts/jobs:
    with db_session() as db:
        ...
    Commits on success, rollbacks on error.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
