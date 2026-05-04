from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.api.v1.dependencies import get_current_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.ml import PredictionResponse
from backend.app.services.prediction_service import PredictionService

router = APIRouter()

@router.get("/tasks/{task_id}/predict", response_model=PredictionResponse)
def predict_completion_time(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        seconds = PredictionService.get_prediction(task_id, current_user.id, db)
        return PredictionResponse(task_id=task_id, predicted_seconds=round(seconds, 2))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))