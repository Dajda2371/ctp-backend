from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user
from datetime import datetime
from typing import Optional

router = APIRouter()

@router.get("/planner/events")
async def list_planner_events(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.PlannerEvent).filter(models.PlannerEvent.user_id == current_user.id)
    
    if start_date:
        query = query.filter(models.PlannerEvent.end_datetime >= start_date)
    if end_date:
        query = query.filter(models.PlannerEvent.start_datetime <= end_date)
        
    events = query.all()
    
    return [
        {
            "id": e.id,
            "task_id": e.task_id,
            "start_datetime": e.start_datetime,
            "end_datetime": e.end_datetime,
            "event_type": e.event_type,
            "title": e.title,
            "description": e.description
        } for e in events
    ]
