# app/services/candidate_service.py

from sqlalchemy.orm import Session
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateCreate

def create_candidate(db: Session, candidate: CandidateCreate) -> Candidate:
    """
    Creates a new candidate in the database.
    """
    # UPDATE the model creation to include the new required field.
    db_candidate = Candidate(
        candidate_name=candidate.candidate_name,
        groups_id=candidate.groups_id
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate