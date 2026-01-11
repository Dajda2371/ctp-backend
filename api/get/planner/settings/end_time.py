from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user

router = APIRouter()

@router.get("/planner/settings/end_time")
async def get_planner_end_time(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    settings = db.query(models.PlannerSettings).filter(models.PlannerSettings.user_id == current_user.id).first()
    end_time = settings.end_time if settings else "17:00"
    return {"end_time": end_time}
