from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    teacher: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    teacher: Optional[str] = None

class CourseOut(CourseBase):
    id: int

    model_config = {"from_attributes": True}
    
class CourseEnrolledOut(CourseBase):
    id: int
    enrolled_at: datetime

    model_config = {"from_attributes": True}