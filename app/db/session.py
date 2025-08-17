# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings

# create_engine is the starting point for any SQLAlchemy application.
# It sets up a "pool" of database connections.
# The pool_pre_ping=True argument helps prevent errors with stale connections.
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# A SessionLocal class is a "factory" for new database sessions.
# Each request to your API will get its own session from this factory.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base will be used as a base class for all of our ORM models (our tables).
# When we create our models in files like `models/question.py`, they will
# inherit from this Base class.
Base = declarative_base()

# Dependency for getting a DB session in API endpoints
def get_db():
    """
    A FastAPI dependency that provides a database session for a single request.
    It ensures the session is always closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()