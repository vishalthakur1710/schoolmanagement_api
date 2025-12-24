from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app import crud, schemas, model
from app.database import get_db
from app.routers.auth import admin_required

router = APIRouter(prefix="/admin", tags=["Admin"])


# =========================================================
# GET ALL USERS (Admin only)
# =========================================================
@router.get("/users", response_model=List[schemas.UserRead])
async def list_users(db: AsyncSession = Depends(get_db), admin: model.User = Depends(admin_required)):
    return await crud.get_all_users(db)


# =========================================================
# GET SINGLE USER BY ID (Admin only)
# =========================================================
@router.get("/users/{user_id}", response_model=schemas.UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db), admin: model.User = Depends(admin_required)):
    user = await crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# =========================================================
# CREATE STUDENT (Admin only)
# =========================================================
@router.post("/students", response_model=schemas.StudentRead)
async def create_student(student: schemas.StudentCreate, db: AsyncSession = Depends(get_db), admin: model.User = Depends(admin_required)):
    return await crud.create_student(db, student)


# =========================================================
# CREATE TEACHER (Admin only)
# =========================================================
@router.post("/teachers", response_model=schemas.TeacherRead)
async def create_teacher(teacher: schemas.TeacherCreate, db: AsyncSession = Depends(get_db), admin: model.User = Depends(admin_required)):
    return await crud.create_teacher(db, teacher)


# =========================================================
# CREATE CLASS (Admin only)
# =========================================================
@router.post("/classes", response_model=schemas.ClassRead)
async def create_class(cls: schemas.ClassCreate, db: AsyncSession = Depends(get_db), admin: model.User = Depends(admin_required)):
    return await crud.create_class(db, cls)


# =========================================================
# CREATE SUBJECT (Admin only)
# =========================================================
@router.post("/subjects", response_model=schemas.SubjectRead)
async def create_subject(subject: schemas.SubjectCreate, db: AsyncSession = Depends(get_db), admin: model.User = Depends(admin_required)):
    return await crud.create_subject(db, subject)


# =========================================================
# LIST ALL CLASSES (Admin only)
# =========================================================
@router.get("/classes", response_model=List[schemas.ClassRead])
async def list_classes(db: AsyncSession = Depends(get_db), admin: model.User = Depends(admin_required)):
    return await crud.get_all_classes(db)


# =========================================================
# LIST ALL SUBJECTS (Admin only)
# =========================================================
@router.get("/subjects", response_model=List[schemas.SubjectRead])
async def list_subjects(db: AsyncSession = Depends(get_db), admin: model.User = Depends(admin_required)):
    return await crud.get_all_subjects(db)
