# app/api/v1/endpoints/votes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.vote import VoteEventCreate, VoteEventRead, VoteCast, VoteCastRead
from app.services import vote_service

router = APIRouter()

@router.post("/", response_model=VoteEventRead, status_code=201)
def create_new_vote_event(
    *,
    db: Session = Depends(get_db),
    vote_in: VoteEventCreate
):
    """
    Create a new voting event.
    """
    try:
        vote_event = vote_service.create_vote_event(db=db, vote_event=vote_in)
        return vote_event
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{vote_id}/cast/", response_model=VoteCastRead)
def cast_new_vote(
    *,
    db: Session = Depends(get_db),
    vote_id: int,
    vote_cast_in: VoteCast
):
    """
    Cast a vote in a specific voting event.
    """
    try:
        vote_record = vote_service.cast_vote(db=db, vote_id=vote_id, vote_cast=vote_cast_in)
        return vote_record
    except ValueError as e:
        # This handles "Voter not found" or "already voted" errors
        raise HTTPException(status_code=400, detail=str(e))