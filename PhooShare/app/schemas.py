from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    """
    Base schema for user details.
    """
    email: str

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str

class User(UserBase):
    """
    Schema for returning user details.
    """
    id: int
    is_active: bool
    role: str

    class Config:
        orm_mode = True

class PhotoBase(BaseModel):
    """
    Base schema for photo details.
    """
    url: str

class PhotoCreate(PhotoBase):
    """
    Schema for creating a new photo.
    """
    description: Optional[str] = None

class Photo(PhotoBase):
    """
    Schema for returning photo details.
    """
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    """
    Base schema for comment details.
    """
    text: str

class CommentCreate(CommentBase):
    """
    Schema for creating a new comment.
    """
    pass

class Comment(CommentBase):
    """
    Schema for returning comment details.
    """
    id: int
    photo_id: int
    author_id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    """
    Schema for returning JWT tokens.
    """
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema for storing JWT token data.
    """
    username: Optional[str] = None
