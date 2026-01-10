from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import auth_utils
from .schemas import PasswordChange

router = APIRouter()

@router.post("/change")
async def change_password(
    data: PasswordChange, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth_utils.get_current_user)
):
    # Verify old password
    if not auth_utils.verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect old password"
        )
    
    # Update to new password
    current_user.hashed_password = auth_utils.get_password_hash(data.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}
