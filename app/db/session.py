# app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# This part remains the same. It sets up the connection engine.
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# This also remains the same. It's our session factory.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This dependency is perfect. We'll use it in our endpoints later.
def get_db():
    """
    FastAPI dependency to provide a database session per request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()