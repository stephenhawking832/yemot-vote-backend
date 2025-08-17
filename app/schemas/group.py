# app/schemas/group.py

from pydantic import BaseModel, ConfigDict

class GroupCreate(BaseModel):
    group_name: str

class GroupRead(BaseModel):
    groups_id: int
    group_name: str | None

    # This is the new way for Pydantic V2
    model_config = ConfigDict(from_attributes=True)