# app/api/v1/endpoints/groups.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.group import GroupCreate, GroupRead
from app.services import group_service

router = APIRouter()

@router.post("/", response_model=GroupRead, status_code=201)
def create_new_group(
    *,
    db: Session = Depends(get_db),
    group_in: GroupCreate
):
    """
    Create a new group.
    """
    group = group_service.create_group(db=db, group=group_in)
    return group