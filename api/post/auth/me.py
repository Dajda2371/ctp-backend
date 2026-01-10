from fastapi import APIRouter, Depends
import models
import auth_utils

router = APIRouter()

@router.get("/me")
async def get_me(current_user: models.User = Depends(auth_utils.get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role
    }
