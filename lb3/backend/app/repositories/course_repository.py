from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models import Course
from typing import Optional, Dict, Any

class CourseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 100):
        stmt = select(Course).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, course_id: int):
        stmt = select(Course).where(Course.id == course_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, title: str, description: Optional[str], teacher: Optional[str]):
        course = Course(title=title, description=description, teacher=teacher)
        self.db.add(course)
        await self.db.flush()
        await self.db.refresh(course)
        return course

    async def update(self, course_id: int, data: Dict[str, Any]):
        stmt = update(Course).where(Course.id == course_id).values(**data)
        await self.db.execute(stmt)
        await self.db.commit()
        return await self.get_by_id(course_id)

    async def delete(self, course_id: int):
        stmt = delete(Course).where(Course.id == course_id)
        await self.db.execute(stmt)
        await self.db.commit()
        return True