from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import uuid

class Education(BaseModel):
    level: str  # e.g., "secondary", "higher-secondary", "graduation", etc.
    institution: str
    score: float  # CGPA or percentage
    year_completed: int

class UserProfile(BaseModel):
    full_name: str
    age: int
    skills: List[str]
    experience: str
    education: List[Education]

class UserBase(BaseModel):
    email: EmailStr

class User(UserBase):
    id: str
    created_at: datetime
    profile: Optional[UserProfile] = None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None

class ChatMessage(BaseModel):
    id: str
    user_id: str
    message: str
    response: str
    created_at: datetime

    class Config:
        from_attributes = True

def create_user_document(email: str) -> dict:
    return {
        "id": str(uuid.uuid4()),      # Unique user ID
        "email": email,               # User's email address
        "created_at": datetime.utcnow(), # Account creation timestamp
        "profile": None
    } 