from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    """
    User model for storing user details.
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  # user, moderator, admin
    
    photos = relationship("Photo", back_populates="owner")
    comments = relationship("Comment", back_populates="author")

class Photo(Base):
    """
    Photo model for storing photo details.
    """
    __tablename__ = 'photos'
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    owner = relationship("User", back_populates="photos")
    comments = relationship("Comment", back_populates="photo")

class Comment(Base):
    """
    Comment model for storing comments on photos.
    """
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    created_at = Column(Integer)
    updated_at = Column(Integer)
    photo_id = Column(Integer, ForeignKey('photos.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    
    photo = relationship("Photo", back_populates="comments")
    author = relationship("User", back_populates="comments")
