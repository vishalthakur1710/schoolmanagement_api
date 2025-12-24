from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from sqlalchemy.future import select

from app import crud, schemas, model
from app.database import get_db
from app.routers.auth import admin_required, teacher_required, student_required

router = APIRouter(prefix="/notifications", tags=["Notifications"])


# =========================================================
# CREATE NOTIFICATION (Admin only)
# =========================================================
@router.post("/admin", response_model=schemas.NotificationRead)
async def create_notification_admin(
    data: schemas.NotificationCreate,
    db: AsyncSession = Depends(get_db),
    admin: model.User = Depends(admin_required)
):
    notif = await crud.create_notification(db, data)
    return notif


# =========================================================
# CREATE NOTIFICATION (Teacher only for their classes)
# =========================================================
@router.post("/teacher", response_model=schemas.NotificationRead)
async def create_notification_teacher(
    data: schemas.NotificationCreate,
    db: AsyncSession = Depends(get_db),
    teacher: model.User = Depends(teacher_required)
):
    # Verify teacher is assigned to target class
    if data.target_class_id:
        assignments = await crud.get_teacher_assignments(db, teacher.teacher_profile.id)
        if not any(a.class_id == data.target_class_id for a in assignments):
            raise HTTPException(
                status_code=403,
                detail="You can only send notifications to your assigned classes"
            )
    notif = await crud.create_notification(db, data)
    return notif


# =========================================================
# GET NOTIFICATIONS FOR CURRENT USER
# =========================================================
@router.get("/me", response_model=List[schemas.NotificationRead])
async def get_my_notifications(
    user: model.User = Depends(student_required),  # works for student by default
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_notifications_for_user(db, user)


# =========================================================
# GET ALL NOTIFICATIONS (Admin view)
# =========================================================
@router.get("/all", response_model=List[schemas.NotificationRead])
async def get_all_notifications(
    db: AsyncSession = Depends(get_db),
    admin: model.User = Depends(admin_required)
):
    result = await db.execute(
        select(model.Notification)
    )
    return result.scalars().all()
