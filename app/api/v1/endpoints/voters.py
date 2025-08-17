# app/api/v1/endpoints/voters.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.voter import VoterCreate, VoterRead

from app.db.session import get_db
from app.services import voter_service

router = APIRouter()


@router.post("/", response_model=VoterRead, status_code=201)
def create_new_voter(
    *,
    db: Session = Depends(get_db),
    voter_in: VoterCreate
):
    """
    Create a single new voter.
    """
    try:
        voter = voter_service.create_voter(db=db, voter=voter_in)
        return voter
    except IntegrityError:
        # This error occurs if the phone number is a duplicate
        # or if the groups_id does not exist.
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Voter could not be created. The phone number may already exist or the group ID is invalid.",
        )






@router.post("/upload-csv/", status_code=201)
def upload_voters_csv(
    *,
    db: Session = Depends(get_db),
    csv_file: UploadFile = File(...)
):
    """
    Create new voters from an uploaded CSV file.
    CSV format: voter_name,voter_phone,groups_id
    """
    if not csv_file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV.")

    try:
        # The service expects a file-like object with bytes
        created_count = voter_service.bulk_create_voters_from_csv(db=db, csv_file=csv_file.file)
        return {"message": f"Successfully created {created_count} voters."}
    except IntegrityError as e:
        # This can happen if a group_id doesn't exist or a phone number is duplicated
        raise HTTPException(status_code=409, detail=f"Database integrity error: {e.orig}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")