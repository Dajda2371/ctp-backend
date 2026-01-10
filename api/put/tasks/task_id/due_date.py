from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user
from datetime import datetime
from typing import Optional

router = APIRouter()

class DueDateUpdate(BaseModel):
    due_date: Optional[datetime] = None

@router.put("/tasks/{task_id}/due_date")
async def update_task_due_date(task_id: int, date_update: DueDateUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.due_date = date_update.due_date
    db.commit()
    db.refresh(db_task)
    return db_task
