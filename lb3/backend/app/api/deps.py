from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.core.security import decode_token
from app.models.user import User
from app.repositories import StudentRepository, UserRepository, CourseRepository, EnrollmentRepository
from app.services import PasswordService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

def get_password_service() -> PasswordService:
    return PasswordService()
    
def get_user_repository(
        db: AsyncSession = Depends(get_db),password_service: PasswordService = Depends(get_password_service)
) -> UserRepository:
    return UserRepository(db, password_service)

def get_student_repository(
        db: AsyncSession = Depends(get_db),
        password_service: PasswordService = Depends(get_password_service)
) -> StudentRepository:
    return StudentRepository(db, password_service)

def get_course_repository(db: AsyncSession = Depends(get_db)) -> CourseRepository:
    return CourseRepository(db)

def get_enrollment_repository(db: AsyncSession = Depends(get_db)) -> EnrollmentRepository:
    return EnrollmentRepository(db)
    
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_user_repository)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        if user_id is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await user_repo.get_by_id(int(user_id))
    if user is None:
        raise credentials_exception
    return user

async def get_current_student(
    current_user: User = Depends(get_current_user),
    student_repo: StudentRepository = Depends(get_student_repository)
):
    student = await student_repo.get_by_user_id(current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return student
    
async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return current_user

async def get_current_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user