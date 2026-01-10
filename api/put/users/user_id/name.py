from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user

router = APIRouter()

class NameUpdate(BaseModel):
    name: str

@router.put("/users/{user_id}/name")
async def update_user_name(
    user_id: int, 
    name_update: NameUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.name = name_update.name
    db.commit()
    db.refresh(db_user)
    
    return {
        "id": str(db_user.id),
        "email": db_user.email,
        "name": db_user.name,
        "role": db_user.role
    }
