from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .security import verify_token
from ..db.csv_storage import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Verify the token and get email
        token_data = await verify_token(token)
        
        # Get user from CSV storage
        user = get_user_by_email(token_data["email"])
        
        if user is None:
            raise credentials_exception
            
        return user
        
    except Exception as e:
        raise credentials_exception 