from pydantic import BaseModel, EmailStr
from typing import Optional
from app.schemas.enums import ThemePreference

class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserOut(UserBase):
    id: int
    theme_preference: ThemePreference = ThemePreference.LIGHT

class UserUpdateTheme(BaseModel):
    theme_preference: ThemePreference

class Config:
        orm_mode = True