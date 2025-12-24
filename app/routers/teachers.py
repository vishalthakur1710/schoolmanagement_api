from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app import crud, schemas, model
from app.database import get_db
from app.routers.auth import teacher_required

router = APIRouter(prefix="/teachers", tags=["Teachers"])


# =========================================================
# GET MY PROFILE
# =========================================================
@router.get("/me", response_model=schemas.TeacherRead)
async def get_my_profile(
    user: model.User = Depends(teacher_required),
    db: AsyncSession = Depends(get_db)
):
    teacher = await crud.get_teacher(db, user.teacher_profile.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    return teacher


# =========================================================
# GET MY CLASS ASSIGNMENTS
# =========================================================
@router.get("/assignments", response_model=List[schemas.ClassAssignmentRead])
async def get_my_assignments(
    user: model.User = Depends(teacher_required),
    db: AsyncSession = Depends(get_db)
):
    assignments = await crud.get_teacher_assignments(db, user.teacher_profile.id)
    return assignments


# =========================================================
# GET STUDENTS IN A CLASS
# =========================================================
@router.get("/classes/{class_id}/students", response_model=List[schemas.StudentRead])
async def get_students_in_class(
    class_id: int,
    user: model.User = Depends(teacher_required),
    db: AsyncSession = Depends(get_db)
):
    # Ensure teacher is assigned to this class
    assignments = await crud.get_teacher_assignments(db, user.teacher_profile.id)
    if not any(a.class_id == class_id for a in assignments):
        raise HTTPException(status_code=403, detail="You are not assigned to this class")

    students = await crud.get_students_by_class(db, class_id)
    return students


# =========================================================
# ADD MARKS
# =========================================================
@router.post("/marks", response_model=schemas.MarksRead)
async def add_student_marks(
    marks: schemas.MarksCreate,
    user: model.User = Depends(teacher_required),
    db: AsyncSession = Depends(get_db)
):
    # Ensure teacher is assigned to this class/subject
    assignments = await crud.get_teacher_assignments(db, user.teacher_profile.id)
    if not any(a.class_id == marks.student_id for a in assignments):
        raise HTTPException(status_code=403, detail="You are not assigned to this class/subject")
    return await crud.add_marks(db, marks)


# =========================================================
# MARK ATTENDANCE
# =========================================================
@router.post("/attendance", response_model=schemas.AttendanceRead)
async def mark_student_attendance(
    att: schemas.AttendanceCreate,
    user: model.User = Depends(teacher_required),
    db: AsyncSession = Depends(get_db)
):
    # Optional: check assignment
    return await crud.mark_attendance(db, att)


# =========================================================
# ADD BEHAVIOR
# =========================================================
@router.post("/behavior", response_model=schemas.BehaviorRead)
async def add_student_behavior(
    behavior: schemas.BehaviorCreate,
    user: model.User = Depends(teacher_required),
    db: AsyncSession = Depends(get_db)
):
    return await crud.add_behavior(db, behavior)


# =========================================================
# GET NOTIFICATIONS
# =========================================================
@router.get("/notifications", response_model=List[schemas.NotificationRead])
async def get_notifications(
    user: model.User = Depends(teacher_required),
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_notifications_for_user(db, user)
