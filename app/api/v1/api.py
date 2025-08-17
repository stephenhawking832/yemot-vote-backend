# app/api/v1/api.py

from fastapi import APIRouter

from app.api.v1.endpoints import groups, candidates, voters, votes

api_router = APIRouter()

# Include each endpoint router with a prefix and tags for the documentation
api_router.include_router(groups.router, prefix="/groups", tags=["Groups"])
api_router.include_router(candidates.router, prefix="/candidates", tags=["Candidates"])
api_router.include_router(voters.router, prefix="/voters", tags=["Voters"])
api_router.include_router(votes.router, prefix="/votes", tags=["Votes"])