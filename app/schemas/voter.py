# app/schemas/voter.py

from pydantic import BaseModel, ConfigDict

class VoterBase(BaseModel):
    voter_name: str | None
    voter_phone: str
    groups_id: int

class VoterCreate(VoterBase):
    pass

class VoterRead(VoterBase):
    voters_id: int

    model_config = ConfigDict(from_attributes=True)