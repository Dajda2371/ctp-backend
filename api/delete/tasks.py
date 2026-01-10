from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user

router = APIRouter()

@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    
    return {"message": "Task deleted successfully"}

@router.delete("/tasks/{task_id}/photos/{photo_index}")
async def delete_task_photo(
    task_id: int, 
    photo_index: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    photos = list(db_task.photos)
    if photo_index < 0 or photo_index >= len(photos):
        raise HTTPException(status_code=404, detail="Photo not found at this index")
    
    photos.pop(photo_index)
    db_task.photos = photos
    
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}/assignee")
async def delete_task_assignee(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.assignee = None
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}/description")
async def delete_task_description(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.description = None
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}/due_date")
async def delete_task_due_date(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.due_date = None
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}/photos")
async def delete_task_photos(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.photos = []
    db.commit()
    db.refresh(db_task)
    return db_task

