from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud, auth_utils as auth
from app.db import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Photo)
def create_photo(photo: schemas.PhotoCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    """
    Create a new photo for the current user.
    """
    return crud.create_photo(db=db, photo=photo, user_id=current_user.id)
