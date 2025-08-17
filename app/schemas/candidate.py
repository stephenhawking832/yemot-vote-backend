# app/schemas/candidate.py

from pydantic import BaseModel, ConfigDict

class CandidateCreate(BaseModel):
    candidate_name: str

class CandidateRead(BaseModel):
    candidates_id: int
    candidate_name: str | None

    model_config = ConfigDict(from_attributes=True)