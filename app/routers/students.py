from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app import crud, schemas, model
from app.database import get_db
from app.routers.auth import student_required

router = APIRouter(prefix="/students", tags=["Students"])


# =========================================================
# GET MY PROFILE
# =========================================================
@router.get("/me", response_model=schemas.StudentRead)
async def get_my_profile(
    user: model.User = Depends(student_required),
    db: AsyncSession = Depends(get_db)
):
    student = await crud.get_student(db, user.student_profile.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return student


# =========================================================
# GET MY MARKS
# =========================================================
@router.get("/marks", response_model=List[schemas.MarksRead])
async def get_my_marks(
    user: model.User = Depends(student_required),
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_student_marks(db, user.student_profile.id)


# =========================================================
# GET MY ATTENDANCE
# =========================================================
@router.get("/attendance", response_model=List[schemas.AttendanceRead])
async def get_my_attendance(
    user: model.User = Depends(student_required),
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_attendance(db, user.student_profile.id)


# =========================================================
# GET MY BEHAVIOR REPORT
# =========================================================
@router.get("/behavior", response_model=List[schemas.BehaviorRead])
async def get_my_behavior(
    user: model.User = Depends(student_required),
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_behavior(db, user.student_profile.id)


# =========================================================
# GET MY NOTIFICATIONS
# =========================================================
@router.get("/notifications", response_model=List[schemas.NotificationRead])
async def get_my_notifications(
    user: model.User = Depends(student_required),
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_notifications_for_user(db, user)

# =========================================================
# GET STUDENT SUMMARY
# =========================================================
@router.get("/summary")
async def get_my_summary(
    user: model.User = Depends(student_required),
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_student_summary(db, user)