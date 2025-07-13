# app/config.py
from pydantic_settings import BaseSettings  

class Settings(BaseSettings):
    database_url: str
    fernet_key: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expires_minutes: int = 60

    class Config:
        env_file = ".env"

settings = Settings()