# app/schemas/voter.py

from pydantic import BaseModel

# Base schema with common fields.
class VoterBase(BaseModel):
    voter_name: str | None
    voter_phone: str
    groups_id: int

# Schema for creating a voter (if we were using a JSON endpoint).
class VoterCreate(VoterBase):
    pass

# Schema for reading voter data.
class VoterRead(VoterBase):
    voters_id: int

    class Config:
        orm_mode = True