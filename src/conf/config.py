# src/conf/config.py
import os
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    sqlalchemy_database_url: str = Field(..., env='DATABASE_URL')
    secret_key: str = Field(..., env='SECRET_KEY')
    algorithm: str = Field(..., env='ALGORITHM')
    cloudinary_name: str = Field(..., env='CLOUDINARY_CLOUD_NAME')
    cloudinary_api_key: str = Field(..., env='CLOUDINARY_API_KEY')
    cloudinary_api_secret: str = Field(..., env='CLOUDINARY_API_SECRET')
    mail_username: str = Field(..., env='MAIL_USERNAME')
    mail_password: str = Field(..., env='MAIL_PASSWORD')
    mail_server: str = Field(..., env='MAIL_SERVER')
    mail_port: int = Field(..., env='MAIL_PORT')
    mail_from: str = Field(..., env='MAIL_FROM')
    access_token_expire_minutes: int = Field(..., env='ACCESS_TOKEN_EXPIRE_MINUTES')
    refresh_token_expire_days: int = Field(..., env='REFRESH_TOKEN_EXPIRE_DAYS')
    mail_starttls: bool = Field(..., env='MAIL_STARTTLS')
    mail_ssl_tls: bool = Field(..., env='MAIL_SSL_TLS')

    class Config:
        env_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env'))
        env_file_encoding = "utf-8"

# Initialize settings
settings = Settings()
