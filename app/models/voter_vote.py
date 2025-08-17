# app/models/voter_vote.py

import datetime
from sqlalchemy import ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class VoterVote(Base):
    __tablename__ = "voters_votes"
    __table_args__ = (UniqueConstraint('voters_id', 'votes_id'),)

    voters_votes_id: Mapped[int] = mapped_column(primary_key=True)
    vote_time: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    voters_id: Mapped[int | None] = mapped_column(ForeignKey("voters.voters_id"))
    votes_id: Mapped[int] = mapped_column(ForeignKey("votes.votes_id"))
    candidates_id: Mapped[int | None] = mapped_column(ForeignKey("candidates.candidates_id"))
    
    # Relationships
    voter: Mapped["Voter"] = relationship()
    vote: Mapped["Vote"] = relationship()
    candidate: Mapped["Candidate"] = relationship()

    def __repr__(self) -> str:
        return f"<VoterVote(id={self.voters_votes_id}, voter_id={self.voters_id}, vote_id={self.votes_id})>"