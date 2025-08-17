# app/schemas/vote.py

from typing import List
from pydantic import BaseModel, ConfigDict

# --- Schemas for the Voting EVENT ---
class VoteEventCreate(BaseModel):
    vote_title: str
    candidate_ids: List[int]

class VoteEventRead(BaseModel):
    votes_id: int
    vote_title: str

    model_config = ConfigDict(from_attributes=True)

# --- Schemas for CASTING a vote ---
class VoteCast(BaseModel):
    voter_phone: str
    candidate_id: int

class VoteCastRead(BaseModel):
    voters_votes_id: int
    votes_id: int
    voters_id: int
    candidates_id: int

    model_config = ConfigDict(from_attributes=True)



class CandidateResult(BaseModel):
    """Represents the results for a single candidate."""
    candidate_id: int
    candidate_name: str
    vote_count: int

class VoteResult(BaseModel):
    """Represents the complete results for a voting event."""
    vote_id: int | None = None
    vote_title: str
    total_votes: int
    breakdown: list[CandidateResult]

# --- Schemas for COMBINING VOTES ---

class VoteCombineRequest(BaseModel):
    """Schema for the request body to combine votes."""
    vote_ids: list[int]