from pydantic import BaseModel
from datetime import datetime

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class EnrollmentOut(BaseModel):
    student_id: int
    course_id: int
    enrolled_at: datetime

    model_config = {"from_attributes": True}