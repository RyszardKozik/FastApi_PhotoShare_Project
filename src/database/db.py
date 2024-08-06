from src.conf.config import settings
from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# SQLAlchemy engine
engine = create_engine(settings.sqlalchemy_database_url)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for getting the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as err_sql:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err_sql))
    finally:
        db.close()
