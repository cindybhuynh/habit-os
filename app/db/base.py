# app/db/base.py
from sqlalchemy.orm import DeclarativeBase # defines shared Base class every SQLAlchemy ORM inherits from


class Base(DeclarativeBase): # Base gains metadata object
    """
    Base class for all SQLAlchemy ORM models.

    Any model that subclasses Base will be registered in Base.metadata,
    which is used to create tables (e.g., Base.metadata.create_all()).
    """
    pass

# metadata object holds schema for all tables inheriting Base
# Alembic reads metadata to update tables