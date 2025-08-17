# app/models/base.py

from sqlalchemy.orm import DeclarativeBase

# This is the modern way to define the Base class.
# All our ORM models will inherit from this.
class Base(DeclarativeBase):
    pass