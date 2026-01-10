from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user

router = APIRouter()

class PriorityUpdate(BaseModel):
    priority: int

@router.put("/tasks/{task_id}/priority")
async def update_task_priority(task_id: int, priority_update: PriorityUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if priority_update.priority < 1 or priority_update.priority > 5:
        raise HTTPException(status_code=400, detail="Priority must be between 1 and 5")
        
    db_task.priority = priority_update.priority
    db.commit()
    db.refresh(db_task)
    return db_task
