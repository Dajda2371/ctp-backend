from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user

router = APIRouter()

class TitleUpdate(BaseModel):
    title: str

@router.put("/tasks/{task_id}/title")
async def update_task_title(task_id: int, title_update: TitleUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.title = title_update.title
    db.commit()
    db.refresh(db_task)
    return db_task
