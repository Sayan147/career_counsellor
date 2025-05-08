from fastapi import HTTPException, status
from ..core.config import get_settings
from ..core.security import create_access_token
from ..models.user import UserLogin, Token
from ..db.csv_storage import get_user_by_email, create_user
from datetime import datetime, timedelta

settings = get_settings()

def get_or_create_user(email: str):
    # Check if user already exists
    user = get_user_by_email(email)
    
    if not user:
        # Create new user
        user = create_user(email)
    
    return user

def login_user(user_login: UserLogin):
    user = get_or_create_user(user_login.email)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]},  # Note: using dict access since CSV returns dict
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"} 