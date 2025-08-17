# app/schemas/candidate.py

from pydantic import BaseModel

# Schema for creating a new candidate.
class CandidateCreate(BaseModel):
    candidate_name: str

# Schema for reading candidate data.
class CandidateRead(BaseModel):
    candidates_id: int
    candidate_name: str | None

    class Config:
        orm_mode = True