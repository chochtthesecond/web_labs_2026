from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from app.models import User
from app.services import PasswordService
from typing import Optional, Dict, Any

class UserRepository:
    def __init__(self, db: AsyncSession, password_service: PasswordService):
        self.db = db
        self.password_service = password_service

    async def get_all(self, skip: int = 0, limit: int = 100):
        stmt = select(User).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, user_id: int):
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
        
    async def get_by_email(self, email: str):
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, email: str, password: str, role: str = "student"):
        hashed = self.password_service.hash(password)
        user = User(email=email, hashed_password=hashed, role=role)
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def update(self, user_id: int, data: Dict[str, Any]):
        stmt = update(User).where(User.id == user_id).values(**data)
        await self.db.execute(stmt)
        await self.db.commit()
        return await self.get_by_id(user_id)

    async def delete(self, user_id: int):
        stmt = delete(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0