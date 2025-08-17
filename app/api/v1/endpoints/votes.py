# app/api/v1/endpoints/votes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.vote import (
    VoteEventCreate, VoteEventRead, VoteCast, VoteCastRead, VoteResult, VoteCombineRequest,
)
from app.services import vote_service
from app.schemas.candidate import CandidateRead

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



@router.get("/{vote_id}/results/", response_model=VoteResult)
def get_results_for_event(
    *,
    db: Session = Depends(get_db),
    vote_id: int,
):
    """
    Get the tallied results for a single voting event.
    """
    try:
        return vote_service.get_vote_results(db=db, vote_id=vote_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{vote_id}/results/by-group/{group_id}/", response_model=VoteResult)
def get_results_for_event_by_group(
    *,
    db: Session = Depends(get_db),
    vote_id: int,
    group_id: int
):
    """
    Get the tallied results for a single voting event, filtered by a specific group.
    """
    try:
        # We reuse the same service function
        return vote_service.get_vote_results(db=db, vote_id=vote_id, group_id=group_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/results/combine/", response_model=VoteResult)
def get_combined_results(
    *,
    db: Session = Depends(get_db),
    payload: VoteCombineRequest,
    group_id: int | None = None # Optional query parameter
):
    """
    Combine the results of multiple vote events.
    - All vote events must share the exact same candidates.
    - Optionally filter the combined results by a group_id.
    """
    try:
        return vote_service.combine_vote_results(
            db=db, vote_ids=payload.vote_ids, group_id=group_id
        )
    except ValueError as e:
        # This will catch validation errors like mismatched candidates
        raise HTTPException(status_code=400, detail=str(e))



@router.get("/{vote_id}/candidates/", response_model=List[CandidateRead])
def get_candidates_in_event(
    *,
    db: Session = Depends(get_db),
    vote_id: int
):
    """
    Get a list of all candidates participating in a specific vote event.
    """
    try:
        candidates = vote_service.get_candidates_for_vote(db=db, vote_id=vote_id)
        return candidates
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
