# backend/app/schemas/task.py
from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    initial_assessment_seconds: Optional[int] = None

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    initial_assessment_seconds: Optional[int] = None