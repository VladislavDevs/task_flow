from pydantic import BaseModel

class PredictionResponse(BaseModel):
    task_id: int
    predicted_seconds: float
    unit: str = "seconds"