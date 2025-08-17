# app/api/v1/endpoints/candidates.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.candidate import CandidateCreate, CandidateRead
from app.services import candidate_service

router = APIRouter()

@router.post("/", response_model=CandidateRead, status_code=201)
def create_new_candidate(
    *,
    db: Session = Depends(get_db),
    candidate_in: CandidateCreate
):
    """
    Create a new candidate.
    """
    candidate = candidate_service.create_candidate(db=db, candidate=candidate_in)
    return candidate