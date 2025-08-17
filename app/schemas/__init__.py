# app/schemas/__init__.py

from .group import GroupCreate, GroupRead
from .candidate import CandidateCreate, CandidateRead
from .voter import VoterCreate, VoterRead
from .vote import VoteEventCreate, VoteEventRead, VoteCast, VoteCastRead