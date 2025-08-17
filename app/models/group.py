# app/models/group.py

from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Group(Base):
    __tablename__ = "groups"

    groups_id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str | None]

    # Relationship to Voter (One-to-Many: One Group has many Voters)
    voters: Mapped[List["Voter"]] = relationship(back_populates="group")
    
    # Relationship to Candidate (Many-to-Many) will be defined via the association table
    # This relationship will be set up in the Candidate model.

    def __repr__(self) -> str:
        return f"<Group(id={self.groups_id}, name='{self.group_name}')>"