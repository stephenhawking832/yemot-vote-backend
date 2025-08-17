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

    # Relationship to Group. `back_populates` points to `candidates` attribute in Group model.
    groups: Mapped[List["Group"]] = relationship(
        secondary=candidates_groups_association, back_populates="candidates"
    )

    # Relationship to Vote. `back_populates` points to `candidates` attribute in Vote model.
    votes: Mapped[List["Vote"]] = relationship(
        secondary="vote_candidates", back_populates="candidates"
    )

    def __repr__(self) -> str:
        return f"<Candidate(id={self.candidates_id}, name='{self.candidate_name}')>"