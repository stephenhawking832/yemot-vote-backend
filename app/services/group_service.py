# app/services/group_service.py

from sqlalchemy.orm import Session
from app.models.group import Group
from app.schemas.group import GroupCreate

def create_group(db: Session, group: GroupCreate) -> Group:
    """
    Creates a new group in the database.

    Args:
        db: The SQLAlchemy database session.
        group: The Pydantic schema containing group data.

    Returns:
        The newly created Group SQLAlchemy model instance.
    """
    # Create a new SQLAlchemy model instance from the schema data
    db_group = Group(group_name=group.group_name)
    
    # Add the instance to the session
    db.add(db_group)
    
    # Commit the transaction to the database
    db.commit()
    
    # Refresh the instance to get the new ID from the database
    db.refresh(db_group)
    
    return db_group