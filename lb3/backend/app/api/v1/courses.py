from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_student, get_current_user
from app.database import get_db
from app.models.user import User
from app.models.course import Course
from app.repositories.course_repository import CourseRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.schemas.course import CourseOut, CourseEnrolledOut

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("", response_model=list[CourseOut])
async def list_courses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = CourseRepository(db)
    courses = await repo.get_all()
    return [CourseOut.model_validate(c) for c in courses]

@router.get("/me", response_model=list[CourseEnrolledOut])
async def my_courses(
    current_student: "Student" = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    from app.models.student import Student
    repo = EnrollmentRepository(db)
    courses = await repo.get_courses_for_student(current_student.id)
    return [CourseEnrolledOut(
            id=course.id,
            title=course.title,
            description=course.description,
            teacher=course.teacher,
            enrolled_at=enrolled_at
        )
        for course, enrolled_at in courses]

@router.post("/{course_id}/enroll", status_code=status.HTTP_201_CREATED)
async def enroll_in_course(
    course_id: int,
    current_student: "Student" = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    enrollment_repo = EnrollmentRepository(db)
    course_repo = CourseRepository(db)
    course = await course_repo.get_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    #проверим нет ли записи
    existing = await enrollment_repo.get_enrollments_for_course(course_id)
    if any(e.student_id == current_student.id for e in existing):
        raise HTTPException(status_code=400, detail="Already enrolled")
    await enrollment_repo.create(current_student.id, course_id)
    return {"detail": "Enrolled successfully"}

@router.delete("/{course_id}/enroll", status_code=status.HTTP_204_NO_CONTENT)
async def unenroll_from_course(
    course_id: int,
    current_student: "Student" = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    enrollment_repo = EnrollmentRepository(db)
    #проверим наличие записи
    enrollments = await enrollment_repo.get_enrollments_for_course(course_id)
    exists = any(e.student_id == current_student.id for e in enrollments)
    if not exists:
        raise HTTPException(status_code=404, detail="Not enrolled")
    await enrollment_repo.delete(current_student.id, course_id)
    return None