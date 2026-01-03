# app/db/base.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
# Import all the models, so that Base has them before being
# imported by Alembic