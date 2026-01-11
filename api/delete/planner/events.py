from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user

router = APIRouter()

@router.delete("/planner/events/{event_id}")
async def delete_planner_event(
    event_id: int,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    event = db.query(models.PlannerEvent).filter(
        models.PlannerEvent.id == event_id,
        models.PlannerEvent.user_id == current_user.id
    ).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    db.delete(event)
    db.commit()
    
    return {"message": "Event deleted"}
