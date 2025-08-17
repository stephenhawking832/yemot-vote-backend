# tests/test_services.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.services import group_service
from app.schemas.group import GroupCreate
from app.models.group import Group
# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Pytest fixture to set up and tear down the database
@pytest.fixture()
def db_session():
    """
    Pytest fixture to create a new database session for each test.
    It creates all tables, yields the session, and then drops all tables.
    """
    # Create all tables in the test database
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after the test is done
        Base.metadata.drop_all(bind=engine)



def test_create_group(db_session):
    """
    GIVEN a group creation schema
    WHEN the create_group service is called
    THEN a new Group record should be created in the database
    """
    # GIVEN: Prepare the input data
    group_schema = GroupCreate(group_name="Test Group")

    # WHEN: Call the service function we want to test
    created_group = group_service.create_group(db=db_session, group=group_schema)

    # THEN: Assert the results
    assert created_group is not None
    assert created_group.groups_id is not None  # It should have an ID from the DB
    assert created_group.group_name == "Test Group"

    # You can also query the database directly to double-check
    group_in_db = db_session.query(Group).filter(Group.groups_id == created_group.groups_id).first()
    assert group_in_db is not None
    assert group_in_db.group_name == "Test Group"