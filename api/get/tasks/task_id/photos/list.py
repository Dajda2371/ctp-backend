from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user

router = APIRouter()

@router.get("/tasks/{task_id}/photos")
async def get_task_photos(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    photos = db.query(models.TaskPhoto).filter(models.TaskPhoto.task_id == task_id).all()
    return {
        "photos": [
            {
                "id": photo.id,
                "filename": photo.filename,
                "mime_type": photo.mime_type,
                "created_at": photo.created_at,
                "url": f"/tasks/{task_id}/photos/{photo.id}"
            } for photo in photos
        ]
    }
