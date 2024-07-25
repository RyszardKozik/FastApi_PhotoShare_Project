from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud, auth_utils as auth
from app.db import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, photo_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    """
    Create a new comment for the current user on a photo.
    """
    return crud.create_comment(db=db, comment=comment, user_id=current_user.id, photo_id=photo_id)
