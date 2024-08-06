from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.conf.config import settings 
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import users as repository_users
from src.database.models import User
from src.conf.config import settings

class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    @classmethod
    def token_decode(cls, token: str) -> dict:
        """
        Try to decode the token

        Arguments:
            token (str): token to decode

        Returns:
            dict with the results of decoded token.
        """
        try:
            return jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
        except JWTError:
            raise cls.credentials_exception

    @classmethod
    async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
        """
        The create_access_token function creates a new access token for the user.

        Arguments:
            data (dict): A dictionary containing the user's information.
            expires_delta (Optional[float]): The number of seconds until the token expires, defaults to None.

        Returns:
            A token that is encoded with the data, current time, expiry time, and scope.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(seconds=expires_delta) if expires_delta else datetime.utcnow() + timedelta(hours=1)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt

    @classmethod
    async def create_refresh_token(cls, data: dict, expires_delta: Optional[float] = None) -> str:
        """
        The create_refresh_token function creates a refresh token for the user.

        Arguments:
            data (dict): A dictionary containing the user's information.
            expires_delta (Optional[float]): Set the expiration time of the refresh token.

        Returns:
            An encoded refresh token.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(seconds=expires_delta) if expires_delta else datetime.utcnow() + timedelta(days=7)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt

    @classmethod
    async def get_current_user(cls, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
        """
        The get_current_user function is a dependency that will be used in the
        protected endpoints. It takes a token as an argument and returns the user
        if it's valid, or raises an exception otherwise.

        Arguments:
            token (str): Get the token from the request header.
            db (Session): SQLAlchemy session object for accessing the database.

        Returns:
            A user object if the token is valid.
        """
        payload = cls.token_decode(token)
        email: str = payload.get("sub")
        if email is None:
            raise cls.credentials_exception

        token_blacklisted = await repository_users.is_blacklisted_token(token, db)
        if token_blacklisted:
            raise cls.credentials_exception

        user = await repository_users.get_user_by_email(email, db)
        if user is None:
            raise cls.credentials_exception
        return user

    @classmethod
    async def decode_refresh_token(cls, refresh_token: str) -> str:
        """
        The decode_refresh_token function is used to decode the refresh token.

        Arguments:
            refresh_token (str): Pass the refresh token to the function.

        Returns:
            The email of the user that is associated with the refresh token.
        """
        payload = cls.token_decode(refresh_token)
        if payload['scope'] == 'refresh_token':
            email = payload['sub']
            return email
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')

auth_service = Auth()
