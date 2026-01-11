from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user
from pydantic import BaseModel

router = APIRouter()

class EndTimeUpdate(BaseModel):
    end_time: str

@router.put("/planner/settings/end_time")
async def update_planner_end_time(
    update: EndTimeUpdate,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    settings = db.query(models.PlannerSettings).filter(models.PlannerSettings.user_id == current_user.id).first()
    if not settings:
        settings = models.PlannerSettings(user_id=current_user.id)
        db.add(settings)
    
    settings.end_time = update.end_time
    db.commit()
    db.refresh(settings)
    
    return {"end_time": settings.end_time}
