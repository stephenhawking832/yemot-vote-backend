# app/schemas/group.py

from pydantic import BaseModel

# Schema for the data required when CREATING a group.
# We only need the name.
class GroupCreate(BaseModel):
    group_name: str

# Schema for the data returned when READING a group.
# This will be used as the response model in the API endpoint.
class GroupRead(BaseModel):
    groups_id: int
    group_name: str | None

    class Config:
        # This allows Pydantic to read the data from our SQLAlchemy model objects.
        orm_mode = True