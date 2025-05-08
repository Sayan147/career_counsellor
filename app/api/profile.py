from fastapi import APIRouter, Depends, HTTPException, status
from ..core.dependencies import get_current_user
from ..models.user import UserProfile
from ..db.csv_storage import update_user_profile, get_user_profile

router = APIRouter()

@router.get("/me")
async def get_profile(current_user: dict = Depends(get_current_user)):
    try:
        profile = get_user_profile(current_user["id"])
        return profile if profile else {}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/update")
async def update_profile(
    profile: UserProfile,
    current_user: dict = Depends(get_current_user)
):
    try:
        success = update_user_profile(current_user["id"], profile)
        if success:
            return {"message": "Profile updated successfully"}
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 