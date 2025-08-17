# app/schemas/vote.py

from typing import List
from pydantic import BaseModel

# --- Schemas for the Voting EVENT ---

# Schema for creating a new voting event.
# We need a title and a list of candidate IDs participating.
class VoteEventCreate(BaseModel):
    vote_title: str
    candidate_ids: List[int]

# Schema for reading a voting event's data.
class VoteEventRead(BaseModel):
    votes_id: int
    vote_title: str

    class Config:
        orm_mode = True


# --- Schemas for CASTING a vote ---

# Schema for the data needed when a voter casts their vote.
# We identify the voter by phone and they choose one candidate ID.
class VoteCast(BaseModel):
    voter_phone: str
    candidate_id: int

# Schema for the confirmation response after a successful vote.
class VoteCastRead(BaseModel):
    voters_votes_id: int
    votes_id: int
    voters_id: int
    candidates_id: int

    class Config:
        orm_mode = True