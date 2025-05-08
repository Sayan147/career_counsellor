from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # JWT settings
    SECRET_KEY: str = "your-secure-secret-key-here"  # Change this in production!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Google API settings
    GOOGLE_API_KEY: str
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 