import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from dotenv import load_dotenv
import os

from src.database.db import get_db
from src.routes import users, auth, comments, tags, images, ratings

# Load environment variables from .env file
load_dotenv()

# Access environment variables
database_url = os.getenv("DATABASE_URL")
secret_key = os.getenv("SECRET_KEY")

# Create FastAPI instance
app = FastAPI()

# Include routers with the '/api' prefix
app.include_router(users.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(comments.router, prefix='/api')
app.include_router(images.router, prefix='/api')
app.include_router(tags.router, prefix='/api')
app.include_router(ratings.router, prefix='/api')

@app.get("/", description='Main page')
def root():
    """
    Main page definition

    :return: dict: health status
    """
    return {"message": "Welcome to the FAST API from team 6"}

@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    """
    Health Checker

    :param db: database session
    :return: dict: health status
    """
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception:
        raise HTTPException(status_code=500, detail="Error connecting to the database")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
