from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from starlette import status

from src.database.models import Rating, User, Image

async def create_rate(image_id: int, rate: int, db: Session, user: User) -> Rating:
    # Check if the image exists
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found.")
    
    # Prevent users from rating their own images
    if image.user_id == user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Users cannot rate their own images.")
    
    # Check if the user has already rated the image
    already_rated = db.query(Rating).filter(and_(Rating.image_id == image_id, Rating.user_id == user.id)).first()
    if already_rated:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="It`s not possible to rate twice.")
    
    # Create a new rating
    new_rate = Rating(image_id=image_id, rate=rate, user_id=user.id)
    db.add(new_rate)
    db.commit()
    db.refresh(new_rate)
    return new_rate

async def delete_rate(rate_id: int, db: Session, user: User) -> None:
    # Check if the rating exists and delete it
    rate = db.query(Rating).filter(Rating.id == rate_id).first()
    if rate:
        db.delete(rate)
        db.commit()
    return None

async def calculate_rating(image_id: int, db: Session) -> float | None:
    # Calculate the average rating of an image
    rating = db.query(func.avg(Rating.rate)).filter(Rating.image_id == image_id).scalar()
    return rating

async def show_images_by_rating(to_decrease: bool, db: Session, user: User) -> List[Image] | list:
    # Show images sorted by rating in the specified order
    if to_decrease:
        images = db.query(Image, func.avg(Rating.rate).label('rate')).join(Rating).order_by(desc('rate')).group_by(Image).all()
    else:
        images = db.query(Image, func.avg(Rating.rate).label('rate')).join(Rating).order_by('rate').group_by(Image).all()
    rez = [image.Image for image in images]
    return rez
