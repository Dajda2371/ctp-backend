from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user

router = APIRouter()

@router.get("/tasks/{task_id}")
async def get_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_photos = db.query(models.TaskPhoto).filter(models.TaskPhoto.task_id == task_id).all()
    return {
        "id": task.id,
        "site_id": task.site_id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "assignee": task.assignee,
        "created_at": task.created_at,
        "due_date": task.due_date,
        "latitude": task.latitude,
        "longitude": task.longitude,
        "photos": [
            {
                "id": p.id,
                "filename": p.filename,
                "mime_type": p.mime_type,
                "url": f"/tasks/{task.id}/photos/{p.id}"
            } for p in task_photos
        ]
    }
