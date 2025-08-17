# app/services/voter_service.py

import csv
import io
from typing import List
from sqlalchemy.orm import Session
from app.models.voter import Voter
from app.schemas.voter import VoterCreate

def create_voter(db: Session, voter: VoterCreate) -> Voter:
    """
    Creates a single new voter in the database.

    Args:
        db: The SQLAlchemy database session.
        voter: The Pydantic schema containing the voter's data.

    Returns:
        The newly created Voter SQLAlchemy model instance.
    """
    # Create a SQLAlchemy Voter model instance from the schema data
    db_voter = Voter(
        voter_name=voter.voter_name,
        voter_phone=voter.voter_phone,
        groups_id=voter.groups_id
    )
    db.add(db_voter)
    db.commit()
    db.refresh(db_voter)
    return db_voter

def bulk_create_voters_from_csv(db: Session, csv_file: io.BytesIO) -> int:
    """
    Parses a CSV file and creates multiple voters in the database.
    Assumes CSV format: voter_name,voter_phone,groups_id

    Args:
        db: The SQLAlchemy database session.
        csv_file: The uploaded CSV file as a byte stream.

    Returns:
        The number of voters successfully created.
    """
    # Decode the byte stream into a text stream
    stream = io.TextIOWrapper(csv_file, encoding="utf-8")
    
    # Use the csv module to read the data
    reader = csv.reader(stream)
    
    # Skip the header row if there is one
    next(reader, None)
    
    voters_to_create: List[Voter] = []
    for row in reader:
        # Basic validation
        if not row or len(row) < 3:
            continue
            
        voter_name, voter_phone, groups_id_str = row
        
        # Create a Voter model instance for each row
        voter = Voter(
            voter_name=voter_name.strip(),
            voter_phone=voter_phone.strip(),
            groups_id=int(groups_id_str.strip())
        )
        voters_to_create.append(voter)

    if not voters_to_create:
        return 0

    try:
        # Use add_all for efficient bulk insertion
        db.add_all(voters_to_create)
        db.commit()
    except Exception as e:
        # If any voter fails (e.g., duplicate phone), rollback the whole transaction
        db.rollback()
        # Re-raise the exception to be handled by the endpoint
        raise e
        
    return len(voters_to_create)