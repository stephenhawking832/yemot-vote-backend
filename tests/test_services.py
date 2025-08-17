# tests/test_services.py

# Python standard library imports
import io
import datetime
import pytest

# SQLAlchemy imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# App-specific imports
# Base for DB creation
from app.models.base import Base
# All services we are testing
from app.services import group_service, candidate_service, voter_service, vote_service
# All schemas needed for tests
from app.schemas.group import GroupCreate
from app.schemas.candidate import CandidateCreate
from app.schemas.vote import VoteEventCreate, VoteCast
# All models needed for test data setup
from app.models.group import Group
from app.models.candidate import Candidate
from app.models.voter import Voter
from app.models.vote import Vote
from app.models.voter_vote import VoterVote


# --- Test Database Setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Pytest Fixture for DB Session ---
@pytest.fixture()
def db_session():
    """
    Pytest fixture to create a new database session for each test.
    Creates all tables, yields the session, and then drops all tables.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


# --- Test Functions ---

def test_create_group(db_session):
    """
    GIVEN a group creation schema
    WHEN the create_group service is called
    THEN a new Group record should be created in the database
    """
    group_schema = GroupCreate(group_name="Test Group")
    created_group = group_service.create_group(db=db_session, group=group_schema)

    assert created_group is not None
    assert created_group.groups_id is not None
    assert created_group.group_name == "Test Group"
    group_in_db = db_session.get(Group, created_group.groups_id)
    assert group_in_db is not None
    assert group_in_db.group_name == "Test Group"


def test_create_candidate(db_session):
    """
    GIVEN a candidate creation schema
    WHEN the create_candidate service is called
    THEN a new Candidate record should be created in the database
    """
    candidate_schema = CandidateCreate(candidate_name="John Doe")
    created_candidate = candidate_service.create_candidate(db=db_session, candidate=candidate_schema)

    assert created_candidate is not None
    assert created_candidate.candidates_id is not None
    assert created_candidate.candidate_name == "John Doe"
    candidate_in_db = db_session.get(Candidate, created_candidate.candidates_id)
    assert candidate_in_db is not None
    assert candidate_in_db.candidate_name == "John Doe"


def test_bulk_create_voters_from_csv(db_session):
    """
    GIVEN a CSV file in memory and a pre-existing group
    WHEN the bulk_create_voters_from_csv service is called
    THEN multiple Voter records should be created in the database
    """
    test_group = Group(group_name="CSV Test Group")
    db_session.add(test_group)
    db_session.commit()
    group_id = test_group.groups_id

    csv_content = f"voter_name,voter_phone,groups_id\nAlice,111222333,{group_id}\nBob,444555666,{group_id}\n"
    csv_file = io.BytesIO(csv_content.encode("utf-8"))

    created_count = voter_service.bulk_create_voters_from_csv(db=db_session, csv_file=csv_file)

    assert created_count == 2
    voters_in_db = db_session.query(Voter).all()
    assert len(voters_in_db) == 2
    assert voters_in_db[0].voter_name == "Alice"


def test_create_vote_event(db_session):
    """
    GIVEN a vote event schema with valid candidate IDs
    WHEN the create_vote_event service is called
    THEN a new Vote record should be created with associated candidates
    """
    candidate1 = Candidate(candidate_name="Candidate A")
    candidate2 = Candidate(candidate_name="Candidate B")
    db_session.add_all([candidate1, candidate2])
    db_session.commit()

    vote_event_schema = VoteEventCreate(
        vote_title="Presidential Election",
        candidate_ids=[candidate1.candidates_id, candidate2.candidates_id]
    )

    created_event = vote_service.create_vote_event(db=db_session, vote_event=vote_event_schema)

    assert created_event is not None
    assert created_event.vote_title == "Presidential Election"
    assert len(created_event.candidates) == 2


def test_cast_vote(db_session):
    """
    GIVEN a voter, a candidate, and a vote event exist
    WHEN the cast_vote service is called with valid data
    THEN a new VoterVote record should be created
    """
    group = Group(group_name="Test Group")
    voter = Voter(voter_name="Test Voter", voter_phone="999888777", group=group)
    candidate = Candidate(candidate_name="Test Candidate")
    vote_event = Vote(
        vote_title="Test Vote",
        candidates=[candidate],
        vote_date=datetime.datetime.now(datetime.UTC)
    )
    db_session.add_all([group, voter, candidate, vote_event])
    db_session.commit()

    vote_cast_schema = VoteCast(voter_phone="999888777", candidate_id=candidate.candidates_id)

    vote_record = vote_service.cast_vote(db=db_session, vote_id=vote_event.votes_id, vote_cast=vote_cast_schema)

    assert vote_record is not None
    assert vote_record.voters_id == voter.voters_id
    assert vote_record.candidates_id == candidate.candidates_id


def test_cast_vote_prevents_double_voting(db_session):
    """
    GIVEN a voter has already voted
    WHEN the cast_vote service is called a second time
    THEN it should raise a ValueError
    """
    group = Group(group_name="Test Group")
    voter = Voter(voter_name="Test Voter", voter_phone="999888777", group=group)
    candidate = Candidate(candidate_name="Test Candidate")
    vote_event = Vote(
        vote_title="Test Vote",
        candidates=[candidate],
        vote_date=datetime.datetime.now(datetime.UTC)
    )
    first_vote = VoterVote(voter=voter, vote=vote_event, candidate=candidate)
    db_session.add_all([group, voter, candidate, vote_event, first_vote])
    db_session.commit()

    vote_cast_schema = VoteCast(voter_phone="999888777", candidate_id=candidate.candidates_id)

    with pytest.raises(ValueError, match="already voted"):
        vote_service.cast_vote(db=db_session, vote_id=vote_event.votes_id, vote_cast=vote_cast_schema)