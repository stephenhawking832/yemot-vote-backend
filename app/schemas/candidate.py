# app/schemas/candidate.py

from pydantic import BaseModel, ConfigDict

class CandidateCreate(BaseModel):
    candidate_name: str
    groups_id: int

class CandidateRead(BaseModel):
    candidates_id: int
    candidate_name: str | None
    groups_id: int

    model_config = ConfigDict(from_attributes=True)