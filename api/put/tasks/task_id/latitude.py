from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user

router = APIRouter()

class LatitudeUpdate(BaseModel):
    latitude: float

@router.put("/tasks/{task_id}/latitude")
async def update_task_latitude(task_id: int, lat_update: LatitudeUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.latitude = lat_update.latitude
    db.commit()
    db.refresh(db_task)
    return db_task
