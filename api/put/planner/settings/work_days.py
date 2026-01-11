from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user
from pydantic import BaseModel

router = APIRouter()

class WorkDaysUpdate(BaseModel):
    work_days: str

@router.put("/planner/settings/work_days")
async def update_planner_work_days(
    update: WorkDaysUpdate,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    settings = db.query(models.PlannerSettings).filter(models.PlannerSettings.user_id == current_user.id).first()
    if not settings:
        settings = models.PlannerSettings(user_id=current_user.id)
        db.add(settings)
    
    settings.work_days = update.work_days
    db.commit()
    db.refresh(settings)
    
    return {"work_days": settings.work_days}
