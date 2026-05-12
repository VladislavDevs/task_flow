# backend/app/schemas/task.py
from pydantic import BaseModel
from typing import Optional
from app.models.task import TaskStatus

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


class TaskOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    status: TaskStatus
    initial_assessment_seconds: Optional[int] = None
    final_assessment_seconds: Optional[int] = None
    category_id: Optional[int] = None
    user_id: int

    class Config:
        orm_mode = True


class TaskListOut(BaseModel):
    total: int
    items: list[TaskOut]