# app/models/voter.py

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Voter(Base):
    __tablename__ = "voters"

    voters_id: Mapped[int] = mapped_column(primary_key=True)
    voter_name: Mapped[str | None]
    voter_phone: Mapped[str | None] = mapped_column(unique=True)
    groups_id: Mapped[int] = mapped_column(ForeignKey("groups.groups_id"))

    # Relationship to Group (Many-to-One: A Voter belongs to one Group)
    group: Mapped["Group"] = relationship(back_populates="voters")

    def __repr__(self) -> str:
        return f"<Voter(id={self.voters_id}, name='{self.voter_name}')>"