# app/db/base.py
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    Any model that subclasses Base will be registered in Base.metadata,
    which is used to create tables (e.g., Base.metadata.create_all()).
    """
    pass
