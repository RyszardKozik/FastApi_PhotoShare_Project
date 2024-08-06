from fastapi import Depends, HTTPException, status, APIRouter, Security, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas.users import UserModel, UserResponse, TokenModel
from src.repository import users as repository_users

router = APIRouter(prefix="/auth", tags=['auth'])
security = HTTPBearer()

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, request: Request, db: Session = Depends(get_db)):
    """
    Create a new user account.
    """
    # Import auth_service within the function to avoid circular import issues
    from src.services.auth import auth_service
    
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password_checksum = auth_service.pwd_context.hash(body.password_checksum)
    new_user = await repository_users.create_user(body, db)
    return new_user

@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a user and return access and refresh tokens.
    """
    # Import auth_service within the function to avoid circular import issues
    from src.services.auth import auth_service
    
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None or not auth_service.pwd_context.verify(body.password, user.password_checksum):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Security(security),
                 db: Session = Depends(get_db)):
    """
    Logout a user by invalidating their JWT token.
    """
    token = credentials.credentials
    await repository_users.add_to_blacklist(token, db)
    return {"message": "USER_IS_LOGOUT"}

@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    """
    Refresh the access token using a valid refresh token.
    """
    from src.services.auth import auth_service
    
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
