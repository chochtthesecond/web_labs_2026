from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.deps import (
    get_current_admin_user as require_admin,
    get_student_repository,
    get_course_repository,
    get_enrollment_repository,
)
from app.database import get_db
from app.models import User
from app.schemas.course import CourseCreate, CourseUpdate, CourseOut
from app.schemas.student import StudentCreateWithUser, StudentUpdate, StudentOut
from app.schemas.enrollment import EnrollmentCreate, EnrollmentOut
from app.repositories import StudentRepository, CourseRepository, EnrollmentRepository

router = APIRouter(prefix="/admin", tags=["Admin"])

#Студенты
@router.get("/students", response_model=List[StudentOut])
async def list_students(
    skip: int = 0,
    limit: int = 100,
    student_repo: StudentRepository = Depends(get_student_repository),
    _=Depends(require_admin)
):
    students = await student_repo.get_all(skip, limit)
    
    result = []
    for s in students:
        result.append(StudentOut(
            id=s.id,
            name=s.name,
            phone=s.phone,
            user_id=s.user_id,
            email=s.user.email,
            created_at=s.user.created_at,
            role=s.user.role
        ))
    return result

@router.get("/students/{student_id}", response_model=StudentOut)
async def get_student(
    student_id: int,
    student_repo: StudentRepository = Depends(get_student_repository),
    _=Depends(require_admin)
):
    student = await student_repo.get_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student = StudentOut(
        id=student.id,
        name=student.name,
        phone=student.phone,
        user_id=student.user_id,
        email=student.user.email,
        created_at=student.user.created_at,
        role=student.user.role
    )
    return student

@router.post("/students", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
async def create_student(
    student_in: StudentCreateWithUser,
    db: AsyncSession = Depends(get_db),
    student_repo: StudentRepository = Depends(get_student_repository),
    _=Depends(require_admin)
):
    try:
        student = await student_repo.create_with_user(
            email=student_in.email,
            password=student_in.password,
            name=student_in.name,
            phone=student_in.phone,
            role=student_in.role
        )
        await db.commit()
    #
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
        
    return StudentOut(
        id=student.id,
        name=student.name,
        phone=student.phone,
        user_id=student.user_id,
        email=student.user.email,
        created_at=student.user.created_at,
        role=student.user.role
    )

@router.put("/students/{student_id}", response_model=StudentOut)
async def update_student(
    student_id: int,
    student_in: StudentUpdate,
    db: AsyncSession = Depends(get_db),
    student_repo: StudentRepository = Depends(get_student_repository),
    _=Depends(require_admin)
):
    existing = await student_repo.get_by_id(student_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = student_in.model_dump(exclude_unset=True)
    try:
        updated = await student_repo.update(student_id, update_data)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already in use")

    return StudentOut(
        id=updated.id,
        name=updated.name,
        phone=updated.phone,
        user_id=updated.user_id,
        email=updated.user.email,
        created_at=updated.user.created_at,
        role=updated.user.role
    )

@router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: int,
    student_repo: StudentRepository = Depends(get_student_repository),
    _=Depends(require_admin)
):
    deleted = await student_repo.delete(student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return None

#Курсы
@router.get("/courses", response_model=List[CourseOut])
async def list_courses(
    skip: int = 0,
    limit: int = 100,
    course_repo: CourseRepository = Depends(get_course_repository),
    _=Depends(require_admin)
):
    courses = await course_repo.get_all(skip, limit)
    return courses

@router.get("/courses/{course_id}", response_model=CourseOut)
async def get_course(
    course_id: int,
    course_repo: CourseRepository = Depends(get_course_repository),
    _=Depends(require_admin)
):
    course = await course_repo.get_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/courses/{course_id}/students", response_model=List[StudentOut])
async def get_course_students(
    course_id: int,
    course_repo: CourseRepository = Depends(get_course_repository),
    enrollment_repo: EnrollmentRepository = Depends(get_enrollment_repository),
    _=Depends(require_admin)
):
    course = await course_repo.get_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
        
    students = await enrollment_repo.get_students_for_course(course_id)

    return [
        StudentOut(
            id=s.id,
            name=s.name,
            phone=s.phone,
            user_id=s.user_id,
            email=s.user.email,
            created_at=s.user.created_at,
            role=s.user.role
        )
        for s in students
    ]
    
@router.post("/courses", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_in: CourseCreate,
    db: AsyncSession = Depends(get_db),
    course_repo: CourseRepository = Depends(get_course_repository),
    _=Depends(require_admin)
):
    course = await course_repo.create(
        title=course_in.title,
        description=course_in.description,
        teacher=course_in.teacher
    )
    await db.commit()
    return course

@router.put("/courses/{course_id}", response_model=CourseOut)
async def update_course(
    course_id: int,
    course_in: CourseUpdate,
    course_repo: CourseRepository = Depends(get_course_repository),
    _=Depends(require_admin)
):
    existing = await course_repo.get_by_id(course_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Course not found")
    update_data = course_in.model_dump(exclude_unset=True)
    updated = await course_repo.update(course_id, update_data)
    return updated

@router.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: int,
    course_repo: CourseRepository = Depends(get_course_repository),
    _=Depends(require_admin)
):
    deleted = await course_repo.delete(course_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Course not found")
    return None

#Поступления
@router.post("/enrollments", response_model=EnrollmentOut, status_code=status.HTTP_201_CREATED)
async def create_enrollment(
    enrollment_in: EnrollmentCreate,
    enrollment_repo: EnrollmentRepository = Depends(get_enrollment_repository),
    _=Depends(require_admin)
):
    #проверим что студент и курс существуют
    enrollment = await enrollment_repo.create(enrollment_in.student_id, enrollment_in.course_id)
    if not enrollment:
        raise HTTPException(status_code=400, detail="Enrollment already exists or invalid student/course")
    return enrollment

@router.delete("/enrollments/{student_id}/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_enrollment(
    student_id: int,
    course_id: int,
    enrollment_repo: EnrollmentRepository = Depends(get_enrollment_repository),
    _=Depends(require_admin)
):
    deleted = await enrollment_repo.delete(student_id, course_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return None