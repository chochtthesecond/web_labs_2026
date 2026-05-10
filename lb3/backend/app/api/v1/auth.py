from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token, RefreshRequest
from app.api.deps import get_current_active_user, get_user_repository, get_student_repository, get_password_service
from app.repositories import StudentRepository, UserRepository
from app.services import PasswordService

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserOut)
async def register(
        user_data: UserCreate,
        db: AsyncSession = Depends(get_db),
        student_repo: StudentRepository = Depends(get_student_repository)):
    try:
        student = await student_repo.create_with_user(
            email=user_data.email,
            password=user_data.password,
            name=user_data.name,
            phone=user_data.phone,
            role="student"
        )
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

    return student.user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), user_repo: UserRepository = Depends(get_user_repository), password_service: PasswordService = Depends(get_password_service)):
    user = await user_repo.get_by_email(form_data.username)
    if not user or not password_service.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
async def refresh_token(request: RefreshRequest, user_repo: UserRepository = Depends(get_user_repository)):
    try:
        payload = decode_token(request.refresh_token)
        user_id = payload.get("sub")
        token_type = payload.get("type")
        if user_id is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        #проверяем существование пользователя
        user = await user_repo.get_by_id(int(user_id))
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        new_access = create_access_token(data={"sub": str(user.id)})
        new_refresh = create_refresh_token(data={"sub": str(user.id)})
        return {"access_token": new_access, "refresh_token": new_refresh, "token_type": "bearer"}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user