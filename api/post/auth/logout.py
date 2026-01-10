from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import auth_utils

router = APIRouter()

@router.post("/logout")
async def logout(
    token: str = Depends(auth_utils.oauth2_scheme), 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user)
):
    # Add token to blacklist
    blacklisted = models.BlacklistedToken(token=token)
    db.add(blacklisted)
    db.commit()
    
    return {"message": "Successfully logged out"}
