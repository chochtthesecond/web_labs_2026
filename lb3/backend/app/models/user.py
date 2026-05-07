from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    student = "student"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(200), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.student)
    created_at = Column(DateTime, server_default=func.now())

    student = relationship("Student", back_populates="user", uselist=False)