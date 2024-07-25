import os
import sys
from fastapi import FastAPI
from dotenv import load_dotenv
from .db import Base, engine
from .routers import auth, users, photos, comments

# Load environment variables from .env file
load_dotenv()

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize FastAPI application
app = FastAPI()

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(photos.router, prefix="/photos", tags=["photos"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])

@app.get("/")
def read_root():
    """
    Root endpoint.

    Returns:
        dict: A greeting message.
    """
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
