from fastapi import APIRouter, HTTPException, status
from ..models.user import UserLogin, Token
from ..services.auth import login_user
from ..core.config import get_settings

settings = get_settings()
router = APIRouter()

@router.post("/login", response_model=Token)
def login(user_login: UserLogin):
    return login_user(user_login) 