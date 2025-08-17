# tests/test_services.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.services import group_service
from app.schemas.group import GroupCreate
from app.models.group import Group
from app.services import candidate_service
from app.schemas.candidate import CandidateCreate
from app.models.candidate import Candidate
import io
from app.services import voter_service
from app.models.voter import Voter
from app.services import vote_service
from app.schemas.vote import VoteEventCreate, VoteCast
from app.models.vote import Vote
from app.models.voter_vote import VoterVote
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



def test_create_candidate(db_session):
    """
    GIVEN a candidate creation schema
    WHEN the create_candidate service is called
    THEN a new Candidate record should be created in the database
    """
    # GIVEN
    candidate_schema = CandidateCreate(candidate_name="John Doe")

    # WHEN
    created_candidate = candidate_service.create_candidate(db=db_session, candidate=candidate_schema)

    # THEN
    assert created_candidate is not None
    assert created_candidate.candidates_id is not None
    assert created_candidate.candidate_name == "John Doe"
    
    # Check database directly
    candidate_in_db = db_session.query(Candidate).get(created_candidate.candidates_id)
    assert candidate_in_db is not None
    assert candidate_in_db.candidate_name == "John Doe"




def test_bulk_create_voters_from_csv(db_session):
    """
    GIVEN a CSV file in memory and a pre-existing group
    WHEN the bulk_create_voters_from_csv service is called
    THEN multiple Voter records should be created in the database
    """
    # GIVEN: First, we need a group for the voters to belong to.
    test_group = Group(group_name="CSV Test Group")
    db_session.add(test_group)
    db_session.commit()
    db_session.refresh(test_group)
    group_id = test_group.groups_id

    # Create a CSV file in-memory
    csv_content = (
        "voter_name,voter_phone,groups_id\n"
        f"Alice,111222333,{group_id}\n"
        f"Bob,444555666,{group_id}\n"
    )
    csv_file = io.BytesIO(csv_content.encode("utf-8"))

    # WHEN
    created_count = voter_service.bulk_create_voters_from_csv(db=db_session, csv_file=csv_file)

    # THEN
    assert created_count == 2
    
    # Check database directly
    voters_in_db = db_session.query(Voter).all()
    assert len(voters_in_db) == 2
    assert voters_in_db[0].voter_name == "Alice"
    assert voters_in_db[0].voter_phone == "111222333"
    assert voters_in_db[1].voter_name == "Bob"
    assert voters_in_db[1].voter_phone == "444555666"



def test_create_vote_event(db_session):
    """
    GIVEN a vote event schema with valid candidate IDs
    WHEN the create_vote_event service is called
    THEN a new Vote record should be created with associated candidates
    """
    # GIVEN: Create some candidates first
    candidate1 = Candidate(candidate_name="Candidate A")
    candidate2 = Candidate(candidate_name="Candidate B")
    db_session.add_all([candidate1, candidate2])
    db_session.commit()

    vote_event_schema = VoteEventCreate(
        vote_title="Presidential Election",
        candidate_ids=[candidate1.candidates_id, candidate2.candidates_id]
    )

    # WHEN
    created_event = vote_service.create_vote_event(db=db_session, vote_event=vote_event_schema)

    # THEN
    assert created_event is not None
    assert created_event.vote_title == "Presidential Election"
    assert len(created_event.candidates) == 2
    assert created_event.candidates[0].candidate_name == "Candidate A"
    
def test_cast_vote(db_session):
    """
    GIVEN a voter, a candidate, and a vote event exist
    WHEN the cast_vote service is called with valid data
    THEN a new VoterVote record should be created
    """
    # GIVEN: We need a full setup: a group, a voter, a candidate, and a vote event
    group = Group(group_name="Test Group")
    voter = Voter(voter_name="Test Voter", voter_phone="999888777", group=group)
    candidate = Candidate(candidate_name="Test Candidate")
    vote_event = Vote(vote_title="Test Vote", candidates=[candidate])
    db_session.add_all([group, voter, candidate, vote_event])
    db_session.commit()

    vote_cast_schema = VoteCast(
        voter_phone="999888777",
        candidate_id=candidate.candidates_id
    )

    # WHEN
    vote_record = vote_service.cast_vote(
        db=db_session,
        vote_id=vote_event.votes_id,
        vote_cast=vote_cast_schema
    )

    # THEN
    assert vote_record is not None
    assert vote_record.voters_id == voter.voters_id
    assert vote_record.votes_id == vote_event.votes_id
    assert vote_record.candidates_id == candidate.candidates_id
    
def test_cast_vote_prevents_double_voting(db_session):
    """
    GIVEN a voter has already voted
    WHEN the cast_vote service is called a second time for the same voter and event
    THEN it should raise a ValueError
    """
    # GIVEN: A full setup where a vote has already been cast
    group = Group(group_name="Test Group")
    voter = Voter(voter_name="Test Voter", voter_phone="999888777", group=group)
    candidate = Candidate(candidate_name="Test Candidate")
    vote_event = Vote(vote_title="Test Vote", candidates=[candidate])
    # The first vote
    first_vote = VoterVote(voter=voter, vote=vote_event, candidate=candidate)
    db_session.add_all([group, voter, candidate, vote_event, first_vote])
    db_session.commit()

    vote_cast_schema = VoteCast(
        voter_phone="999888777",
        candidate_id=candidate.candidates_id
    )

    # WHEN / THEN: Use pytest.raises to assert that an exception is thrown
    with pytest.raises(ValueError, match="already voted"):
        vote_service.cast_vote(
            db=db_session,
            vote_id=vote_event.votes_id,
            vote_cast=vote_cast_schema
        )

