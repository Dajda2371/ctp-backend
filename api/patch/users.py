from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user
from typing import Optional

router = APIRouter()

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

class RoleUpdate(BaseModel):
    role: str

@router.patch("/users/{user_id}")
async def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_update.dict(exclude_unset=True)
    
    if "role" in update_data:
        valid_roles = ["admin", "property_manager", "facility_manager", "technician", "cleaning"]
        if update_data["role"] not in valid_roles:
            raise HTTPException(status_code=400, detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}")
    
    if "email" in update_data:
        existing_user = db.query(models.User).filter(models.User.email == update_data["email"], models.User.id != user_id).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already taken")

    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    
    return {
        "id": str(db_user.id),
        "email": db_user.email,
        "name": db_user.name,
        "role": db_user.role
    }

@router.patch("/users/{user_id}/role")
async def update_user_role(
    user_id: int, 
    role_update: RoleUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    return await update_user(user_id, UserUpdate(role=role_update.role), db, current_user)
