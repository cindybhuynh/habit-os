# app/db/init_db.py
from app.db.base import Base
from app.db.session import engine

# Import models so they register with Base.metadata
from app.models.habit import Habit  # noqa: F401


def init_db() -> None:
    """
    Creates tables in the database for all models registered on Base.metadata.

    This is a dev-friendly shortcut (no Alembic yet). Once you start changing
    schema over time, you’ll want migrations (Alembic).
    """
    Base.metadata.create_all(bind=engine)
