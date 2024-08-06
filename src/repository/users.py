from datetime import datetime
from sqlalchemy.orm import Session
from libgravatar import Gravatar
from src.database.models import User, BlacklistToken
from src.schemas.users import UserModel

def get_user_by_email(email: str, db: Session) -> User | None:
    """
    Retrieve a user by email.
    """
    return db.query(User).filter_by(email=email).first()

def create_user(body: UserModel, db: Session) -> User:
    """
    Create a new user in the database.

    :param body: UserModel - user data to create a new user
    :param db: Session - database session
    :return: User - created user instance
    """
    # Generate a Gravatar URL for the user
    g = Gravatar(body.email)
    new_user = User(**body.dict(), user_pic_url=g.get_image())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_token(user: User, refresh_token: str | None, db: Session) -> None:
    """
    Update the refresh token for a user.

    :param user: User - user instance to update
    :param refresh_token: str | None - new refresh token value
    :param db: Session - database session
    """
    user.refresh_token = refresh_token
    db.commit()

def add_to_blacklist(token: str, db: Session) -> None:
    """
    Add a JWT token to the blacklist.

    :param token: str - JWT token to add to the blacklist
    :param db: Session - database session
    """
    blacklist_token = BlacklistToken(token=token, added_on=datetime.now())
    db.add(blacklist_token)
    db.commit()
    db.refresh(blacklist_token)

def is_blacklisted_token(token: str, db: Session) -> bool:
    """
    Check if a token is blacklisted.

    :param token: str - JWT token to check
    :param db: Session - database session
    :return: bool - True if token is blacklisted, False otherwise
    """
    blacklist_token = db.query(BlacklistToken).filter(BlacklistToken.token == token).first()
    return blacklist_token is not None
