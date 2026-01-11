from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user
from pydantic import BaseModel

router = APIRouter()

class SettingsUpdate(BaseModel):
    start_time: str
    end_time: str
    work_days: str

@router.get("/planner/settings")
async def get_planner_settings(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    settings = db.query(models.PlannerSettings).filter(models.PlannerSettings.user_id == current_user.id).first()
    if not settings:
        # Return default if not set
        return {
            "start_time": "09:00",
            "end_time": "17:00",
            "work_days": "0,1,2,3,4"
        }
    return {
        "start_time": settings.start_time,
        "end_time": settings.end_time,
        "work_days": settings.work_days
    }

@router.put("/planner/settings")
async def update_planner_settings(
    update: SettingsUpdate,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    settings = db.query(models.PlannerSettings).filter(models.PlannerSettings.user_id == current_user.id).first()
    if not settings:
        settings = models.PlannerSettings(user_id=current_user.id)
        db.add(settings)
    
    settings.start_time = update.start_time
    settings.end_time = update.end_time
    settings.work_days = update.work_days
    
    db.commit()
    db.refresh(settings)
    
    return {
        "start_time": settings.start_time,
        "end_time": settings.end_time,
        "work_days": settings.work_days
    }
