from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user

router = APIRouter()

@router.delete("/tasks/{task_id}/photos")
async def delete_task_photos(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.query(models.TaskPhoto).filter(models.TaskPhoto.task_id == task_id).delete()
    db_task.photos = []
    db.commit()
    return {"detail": "All photos for the task deleted"}
