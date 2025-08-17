# app/models/candidate.py

from typing import List
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

# Define the association table for the candidates<->groups relationship
candidates_groups_association = Table(
    "candidates_groups",
    Base.metadata,
    Column("candidates_groups_id", Integer, primary_key=True),
    Column("candidates_id", Integer, ForeignKey("candidates.candidates_id"), nullable=False),
    Column("groups_id", Integer, ForeignKey("groups.groups_id"), nullable=False),
)

class Candidate(Base):
    __tablename__ = "candidates"

    candidates_id: Mapped[int] = mapped_column(primary_key=True)
    candidate_name: Mapped[str | None]

    # ADD the new foreign key column to groups
    groups_id: Mapped[int] = mapped_column(ForeignKey("groups.groups_id"))

    # CHANGE the relationship from a List["Group"] to a single "Group"
    # This defines the "many-to-one" side of the relationship.
    group: Mapped["Group"] = relationship(back_populates="candidates")

    # The relationship to Vote remains the same
    votes: Mapped[List["Vote"]] = relationship(
        secondary="vote_candidates", back_populates="candidates"
    )

    def __repr__(self) -> str:
        # Update the repr to be more useful
        return f"<Candidate(id={self.candidates_id}, name='{self.candidate_name}', group_id={self.groups_id})>"