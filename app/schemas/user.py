from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
  username: str
  email: EmailStr
  password: str

class UserOut(BaseModel):
  id: int
  username: str
  email: str
  avt_url: Optional[str] = None
  phone: Optional[str] = None
  location: Optional[str] = None
  role: str
  is_active: Optional[bool] = None
  created_at: Optional[datetime] = None

  class Config:
    from_attributes = True