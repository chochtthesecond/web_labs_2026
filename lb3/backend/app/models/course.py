from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    teacher = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())

    enrollments = relationship("CourseEnrollment", back_populates="course", cascade="all, delete-orphan")