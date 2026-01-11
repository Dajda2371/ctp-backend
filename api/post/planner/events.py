from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()

class EventCreate(BaseModel):
    task_id: Optional[int] = None
    start_datetime: datetime
    end_datetime: datetime
    event_type: str # 'work', 'time_off', 'task'
    title: Optional[str] = None
    description: Optional[str] = None

@router.post("/planner/events")
async def create_planner_event(
    event: EventCreate,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    if event.start_datetime >= event.end_datetime:
        raise HTTPException(status_code=400, detail="Start time must be before end time")
        
    new_event = models.PlannerEvent(
        user_id=current_user.id,
        task_id=event.task_id,
        start_datetime=event.start_datetime,
        end_datetime=event.end_datetime,
        event_type=event.event_type,
        title=event.title,
        description=event.description
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    
    return {
        "id": new_event.id,
        "task_id": new_event.task_id,
        "start_datetime": new_event.start_datetime,
        "end_datetime": new_event.end_datetime,
        "event_type": new_event.event_type,
        "title": new_event.title,
        "description": new_event.description
    }
