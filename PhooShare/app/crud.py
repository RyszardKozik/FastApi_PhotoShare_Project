from sqlalchemy.orm import Session
from . import models, schemas
from .auth_utils import get_password_hash

def get_user_by_email(db: Session, email: str):
    """
    Get a user by their email address.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a new user.
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_photo(db: Session, photo: schemas.PhotoCreate, user_id: int):
    """
    Create a new photo.
    """
    db_photo = models.Photo(**photo.dict(), owner_id=user_id)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int, photo_id: int):
    """
    Create a new comment.
    """
    db_comment = models.Comment(**comment.dict(), author_id=user_id, photo_id=photo_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
