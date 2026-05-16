from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
from app.schemas.enums import TaskStatus, TaskPriority

class TaskBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None
    category_id: Optional[int] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    @validator('due_date')
    def validate_date(cls, v):
        if v and v.replace(tzinfo=None) < datetime.now().replace(tzinfo=None):
            raise ValueError("Дата не может быть в прошлом")
        return v
    
class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None

class TaskOut(TaskBase):
    id: int
    status: TaskStatus
    actual_completion_time: Optional[int] = None
    
    class Config:
        orm_mode = True

class TaskListOut(BaseModel):
    total: int
    items: List[TaskOut]