from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user

router = APIRouter()

class EmailUpdate(BaseModel):
    email: str

@router.put("/users/{user_id}/email")
async def update_user_email(
    user_id: int, 
    email_update: EmailUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if email is or has been taken by another user
    existing_user = db.query(models.User).filter(models.User.email == email_update.email, models.User.id != user_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already taken")

    db_user.email = email_update.email
    db.commit()
    db.refresh(db_user)
    
    return {
        "id": str(db_user.id),
        "email": db_user.email,
        "name": db_user.name,
        "role": db_user.role
    }
