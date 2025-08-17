# app/services/vote_service.py

import datetime
from sqlalchemy.orm import Session
from app.models import Vote, Candidate, Voter, VoterVote
from app.schemas.vote import VoteEventCreate, VoteCast

def create_vote_event(db: Session, vote_event: VoteEventCreate) -> Vote:
    """
    Creates a new voting event and associates candidates with it.
    """
    # 1. Find all candidate objects from the provided IDs
    candidates = db.query(Candidate).filter(Candidate.candidates_id.in_(vote_event.candidate_ids)).all()
    if len(candidates) != len(vote_event.candidate_ids):
        raise ValueError("One or more candidate IDs are invalid.")

    # 2. Create the new Vote event
    db_vote_event = Vote(
        vote_title=vote_event.vote_title,
        vote_date=datetime.datetime.utcnow(),
        candidates=candidates  # Associate the candidates
    )
    
    db.add(db_vote_event)
    db.commit()
    db.refresh(db_vote_event)
    
    return db_vote_event

def cast_vote(db: Session, vote_id: int, vote_cast: VoteCast) -> VoterVote:
    """
    Allows a voter to cast their vote, with several validation checks.
    """
    # 1. Find the voter by their phone number
    voter = db.query(Voter).filter(Voter.voter_phone == vote_cast.voter_phone).first()
    if not voter:
        raise ValueError("Voter with this phone number not found.")

    # 2. Check if the voter has already voted in this event
    existing_vote = db.query(VoterVote).filter(
        VoterVote.voters_id == voter.voters_id,
        VoterVote.votes_id == vote_id
    ).first()
    if existing_vote:
        raise ValueError("This voter has already voted in this event.")

    # 3. Create the vote record
    db_voter_vote = VoterVote(
        voters_id=voter.voters_id,
        votes_id=vote_id,
        candidates_id=vote_cast.candidate_id,
        # vote_time is handled by the database default
    )
    
    db.add(db_voter_vote)
    db.commit()
    db.refresh(db_voter_vote)
    
    return db_voter_vote