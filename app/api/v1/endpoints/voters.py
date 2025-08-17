# app/api/v1/endpoints/voters.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.services import voter_service

router = APIRouter()

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