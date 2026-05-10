from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from app.models import User, Student
from app.services import PasswordService
from typing import Optional, Dict, Any

class StudentRepository:
    def __init__(self, db: AsyncSession, password_service: PasswordService):
        self.db = db
        self.password_service = password_service

    async def get_all(self, skip: int = 0, limit: int = 100):
        stmt = select(Student).options(selectinload(Student.user)).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, student_id: int):
        stmt = select(Student).options(selectinload(Student.user)).where(Student.id == student_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
        
    async def get_by_user_id(self, user_id: int):
        #получение студента по id пользователя
        stmt = select(Student).options(selectinload(Student.user)).where(Student.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_with_user(self, email: str, password: str, name: str, phone: Optional[str], role: str = "student"):
        #создание пользователя и профиля студента в одной транзакции
        hashed = self.password_service.hash(password)
        user = User(email=email, hashed_password=hashed, role=role)
        self.db.add(user)
        await self.db.flush() #чтобы получить user.id

        student = Student(user_id=user.id, name=name, phone=phone)
        self.db.add(student)
        await self.db.flush()
        await self.db.refresh(student, attribute_names=["user"])
        return student

    async def update(self, student_id: int, data: Dict[str, Any]):
        #обновляем поля студента
        student_update_data = {k: v for k, v in data.items() if k in ["name", "phone"]}
        if student_update_data:
            stmt = update(Student).where(Student.id == student_id).values(**student_update_data)
            await self.db.execute(stmt)

        #обновляем поля user
        user_update_data = {k: v for k, v in data.items() if k in ["email", "role"]}
        if user_update_data:
            #получим user_id студента
            student = await self.get_by_id(student_id)
            if student:
                stmt = update(User).where(User.id == student.user_id).values(**user_update_data)
                await self.db.execute(stmt)
        await self.db.commit()
        return await self.get_by_id(student_id)

    async def delete(self, student_id: int):
        stmt = select(Student).where(Student.id == student_id).options(selectinload(Student.user))
        result = await self.db.execute(stmt)
        student = result.scalar_one_or_none()
        
        if not student:
            return False
        
        #убираем ссылку на пользователя
        await self.db.delete(student)
        
        #удаляем пользователя
        if student.user:
            await self.db.delete(student.user)
        
        await self.db.commit()
        return True