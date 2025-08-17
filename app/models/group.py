# app/models/group.py

from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Group(Base):
    __tablename__ = "groups"

    groups_id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str | None]

    # Relationship to Voter. `back_populates` points to the `group` attribute in the Voter model.
    voters: Mapped[List["Voter"]] = relationship(back_populates="group")
    
    # Relationship to Candidate. `back_populates` points to the `groups` attribute in the Candidate model.
    candidates: Mapped[List["Candidate"]] = relationship(
        secondary="candidates_groups", back_populates="groups"
    )

    def __repr__(self) -> str:
        return f"<Group(id={self.groups_id}, name='{self.group_name}')>"