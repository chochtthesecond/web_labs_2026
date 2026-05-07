from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models import CourseEnrollment, Course
from typing import Optional

class EnrollmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, student_id: int, course_id: int):
        enrollment = CourseEnrollment(student_id=student_id, course_id=course_id)
        self.db.add(enrollment)
        try:
            await self.db.commit()
            await self.db.refresh(enrollment)
            return enrollment
        except Exception:
            await self.db.rollback()
            return None

    async def delete(self, student_id: int, course_id: int):
        stmt = delete(CourseEnrollment).where(
            CourseEnrollment.student_id == student_id,
            CourseEnrollment.course_id == course_id
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0

    async def get_enrollments_for_course(self, course_id: int):
        stmt = select(CourseEnrollment).where(CourseEnrollment.course_id == course_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()
        
    async def get_courses_for_student(self, student_id: int):
        stmt = (
            select(Course, CourseEnrollment.enrolled_at).join(CourseEnrollment).where(CourseEnrollment.student_id == student_id)
        )
        result = await self.db.execute(stmt)
        return result.all()