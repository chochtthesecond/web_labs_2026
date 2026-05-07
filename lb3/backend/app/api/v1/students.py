from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_student, get_current_user
from app.database import get_db
from app.models.user import User
from app.models.student import Student
from app.repositories.student_repository import StudentRepository
from app.schemas.student import StudentOut, StudentUpdate

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/me", response_model=StudentOut)
async def get_my_profile(
    current_student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    return StudentOut(
        id=current_student.id,
        name=current_student.name,
        phone=current_student.phone,
        email=current_student.user.email,
        role=current_student.user.role,
        created_at=current_student.user.created_at,
        user_id=current_student.user_id,
    )

@router.put("/me", response_model=StudentOut)
async def update_my_profile(
    student_update: StudentUpdate,
    current_student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    update_data = {}
    if student_update.name is not None:
        update_data["name"] = student_update.name
    if student_update.phone is not None:
        update_data["phone"] = student_update.phone 
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
        
    repo = StudentRepository(db)
    updated = await repo.update(current_student.id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return StudentOut(
        id=updated.id,
        name=updated.name,
        phone=updated.phone,
        email=updated.user.email,
        role=updated.user.role,
        created_at=updated.user.created_at,
        user_id=updated.user_id,
    )