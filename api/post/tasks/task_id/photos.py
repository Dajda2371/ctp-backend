from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user
import sys
import os

router = APIRouter()

class PhotoAdd(BaseModel):
    url: str

@router.post("/tasks/{task_id}/photos")
async def add_task_photo(
    task_id: int, 
    photo: PhotoAdd, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update photos list (SQLAlchemy JSON mutation)
    photos = list(db_task.photos) if db_task.photos else []
    photos.append(photo.url)
    db_task.photos = photos
    
    db.commit()
    db.refresh(db_task)
    return db_task
