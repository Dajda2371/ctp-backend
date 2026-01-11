from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user
from pydantic import BaseModel

router = APIRouter()

class StartTimeUpdate(BaseModel):
    start_time: str

@router.put("/planner/settings/start_time")
async def update_planner_start_time(
    update: StartTimeUpdate,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    settings = db.query(models.PlannerSettings).filter(models.PlannerSettings.user_id == current_user.id).first()
    if not settings:
        settings = models.PlannerSettings(user_id=current_user.id)
        db.add(settings)
    
    settings.start_time = update.start_time
    db.commit()
    db.refresh(settings)
    
    return {"start_time": settings.start_time}
