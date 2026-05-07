from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    name: str
    password: str
    phone: Optional[str] = None

class UserOut(UserBase):
    id: int
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}

class UserInDB(UserOut):
    hashed_password: str
    
    model_config = {"from_attributes": True}
    
class UserCreateAdmin(UserCreate):
    role: str = "student"