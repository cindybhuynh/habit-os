# app/db/init_db.py
from app.db.base import Base
from app.db.session import engine

# IMPORTANT: import models so SQLAlchemy registers them on Base.metadata
from app.models import habit  # noqa: F401

def init_db() -> None:
    Base.metadata.create_all(bind=engine)
