# app/models/vote.py

import datetime
from typing import List
from sqlalchemy import Column, ForeignKey, Integer, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

# Define the association table for the votes<->candidates relationship
vote_candidates_association = Table(
    "vote_candidates",
    Base.metadata,
    Column("vote_candidates_id", Integer, primary_key=True),
    Column("votes_id", Integer, ForeignKey("votes.votes_id"), nullable=False),
    Column("candidates_id", Integer, ForeignKey("candidates.candidates_id"), nullable=False),
    UniqueConstraint("votes_id", "candidates_id")
)

class Vote(Base):
    __tablename__ = "votes"

    votes_id: Mapped[int] = mapped_column(primary_key=True)
    vote_title: Mapped[str]
    vote_date: Mapped[datetime.datetime]

    # Relationship to Candidate. `back_populates` points to `votes` attribute in Candidate model.
    candidates: Mapped[List["Candidate"]] = relationship(
        secondary=vote_candidates_association, back_populates="votes"
    )

    def __repr__(self) -> str:
        return f"<Vote(id={self.votes_id}, title='{self.vote_title}')>"