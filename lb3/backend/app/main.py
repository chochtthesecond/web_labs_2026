from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, admin, students, courses

app = FastAPI(title="Smart Title API", version="1.0.0")
    
#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"]
)

#регистрация роутеров
app.include_router(auth.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(students.router, prefix="/api/v1")
app.include_router(courses.router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "ok"}