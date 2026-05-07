from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.schemas.user import UserCreateAdmin, UserBase

class StudentBase(BaseModel):
    name: str
    phone: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentCreateWithUser(StudentBase):
    email: str
    password: str
    role: str = "student"

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

class StudentOut(StudentBase):
    id: int
    email: str
    user_id: int
    created_at: datetime
    role: str

    model_config = {"from_attributes": True}