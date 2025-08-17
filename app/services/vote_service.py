# app/services/vote_service.py

import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Vote, Candidate, Voter, VoterVote, Group
from app.schemas.vote import VoteEventCreate, VoteCast, VoteResult, CandidateResult
from typing import List
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



def get_vote_results(db: Session, vote_id: int, group_id: int | None = None) -> VoteResult:
    """
    Calculates the results for a single vote event, with an optional filter by group.
    """
    # 1. Fetch the vote event to get its title
    vote_event = db.get(Vote, vote_id)
    if not vote_event:
        raise ValueError("Vote event not found.")

    # 2. Build the base query for counting votes
    query = (
        db.query(
            Candidate.candidates_id,
            Candidate.candidate_name,
            func.count(VoterVote.voters_votes_id).label("vote_count"),
        )
        .join(VoterVote, VoterVote.candidates_id == Candidate.candidates_id)
        .filter(VoterVote.votes_id == vote_id)
    )

    # 3. If a group_id is provided, add a filter for it
    if group_id:
        query = query.join(Voter, Voter.voters_id == VoterVote.voters_id).filter(
            Voter.groups_id == group_id
        )

    # 4. Group by candidate and order the results
    results = (
        query.group_by(Candidate.candidates_id, Candidate.candidate_name)
        .order_by(func.count(VoterVote.voters_votes_id).desc())
        .all()
    )

    # 5. Structure the results using our Pydantic schemas
    breakdown = [
        CandidateResult(
            candidate_id=cid, candidate_name=cname, vote_count=count
        )
        for cid, cname, count in results
    ]
    total_votes = sum(item.vote_count for item in breakdown)

    return VoteResult(
        vote_id=vote_id,
        vote_title=vote_event.vote_title,
        total_votes=total_votes,
        breakdown=breakdown,
    )


def combine_vote_results(db: Session, vote_ids: list[int], group_id: int | None = None) -> VoteResult:
    """
    Calculates the combined results for a list of vote events, with an optional filter by group.
    Validates that all events share the exact same set of candidates.
    """
    if not vote_ids or len(vote_ids) < 2:
        raise ValueError("At least two vote IDs are required to combine results.")

    # 1. Validate that all vote events have the same candidates
    votes = db.query(Vote).filter(Vote.votes_id.in_(vote_ids)).all()
    if len(votes) != len(vote_ids):
        raise ValueError("One or more vote IDs are invalid.")
    
    first_candidate_set = {c.candidates_id for c in votes[0].candidates}
    for vote in votes[1:]:
        candidate_set = {c.candidates_id for c in vote.candidates}
        if first_candidate_set != candidate_set:
            raise ValueError(
                f"Cannot combine events. Vote ID {vote.votes_id} has a different set of candidates."
            )

    # 2. The query is very similar to get_vote_results, but filters for multiple IDs
    query = (
        db.query(
            Candidate.candidates_id,
            Candidate.candidate_name,
            func.count(VoterVote.voters_votes_id).label("vote_count"),
        )
        .join(VoterVote, VoterVote.candidates_id == Candidate.candidates_id)
        .filter(VoterVote.votes_id.in_(vote_ids)) # Key difference is here
    )

    if group_id:
        query = query.join(Voter, Voter.voters_id == VoterVote.voters_id).filter(
            Voter.groups_id == group_id
        )

    results = (
        query.group_by(Candidate.candidates_id, Candidate.candidate_name)
        .order_by(func.count(VoterVote.voters_votes_id).desc())
        .all()
    )
    
    # 3. Structure the results
    breakdown = [
        CandidateResult(
            candidate_id=cid, candidate_name=cname, vote_count=count
        )
        for cid, cname, count in results
    ]
    total_votes = sum(item.vote_count for item in breakdown)
    
    combined_title = "Combined Results: " + " & ".join([v.vote_title for v in votes])

    return VoteResult(
        vote_title=combined_title,
        total_votes=total_votes,
        breakdown=breakdown,
    )



def get_candidates_for_vote(db: Session, vote_id: int) -> List[Candidate]:
    """
    Retrieves a list of all candidates participating in a specific vote event.

    Args:
        db: The SQLAlchemy database session.
        vote_id: The ID of the vote event.

    Returns:
        A list of Candidate SQLAlchemy model instances.
    
    Raises:
        ValueError: If the vote event with the given ID is not found.
    """
    # Use session.get for a simple primary key lookup
    vote_event = db.get(Vote, vote_id)

    if not vote_event:
        raise ValueError("Vote event not found.")

    # Thanks to SQLAlchemy relationships, the candidates are already linked.
    # We can just return them directly.
    return vote_event.candidates