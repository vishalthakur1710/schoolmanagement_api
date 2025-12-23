from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from passlib.context import CryptContext
from datetime import date, datetime
import asyncio
from app import model, schemas

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)
# =========================================================
# AUTH HELPERS
# =========================================================
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)


# =========================================================
# USERS CRUD
# =========================================================
async def create_user(db: AsyncSession, user_data: schemas.UserCreate):
    hashed = hash_password(user_data.password)
    new_user = model.User(
        name=user_data.name,
        email=user_data.email,
        password=hashed,
        role=user_data.role,
        is_active=True
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(model.User).where(model.User.email == email))
    return result.scalars().first()


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(model.User).where(model.User.id == user_id))
    return result.scalars().first()


async def get_all_users(db: AsyncSession):
    result = await db.execute(select(model.User))
    return result.scalars().all()


# =========================================================
# STUDENT CRUD
# =========================================================
async def create_student(db: AsyncSession, data: schemas.StudentCreate):
    new_student = model.Student(
        user_id=data.user_id,
        class_id=data.class_id,
        age=data.age,
        sex=data.sex
    )
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return new_student


async def get_student(db: AsyncSession, student_id: int):
    result = await db.execute(
        select(model.Student)
        .where(model.Student.id == student_id)
        .options(joinedload(model.Student.user))
    )
    return result.scalars().first()


async def get_students_by_class(db: AsyncSession, class_id: int):
    result = await db.execute(
        select(model.Student).where(model.Student.class_id == class_id)
    )
    return result.scalars().all()



async def get_student_summary(db: AsyncSession, user: model.User):
    """
    Return profile, marks, attendance, behavior and notifications for a student.
    """
    student_id = user.student_profile.id

    profile_task = get_student(db, student_id)
    marks_task = get_student_marks(db, student_id)
    attendance_task = get_attendance(db, student_id)
    behavior_task = get_behavior(db, student_id)
    notifications_task = get_notifications_for_user(db, user)

    profile, marks, attendance, behavior, notifications = await asyncio.gather(
        profile_task, marks_task, attendance_task, behavior_task, notifications_task
    )

    return {
        "profile": profile,
        "marks": marks,
        "attendance": attendance,
        "behavior": behavior,
        "notifications": notifications,
    }


# =========================================================
# TEACHER CRUD
# =========================================================
async def create_teacher(db: AsyncSession, data: schemas.TeacherCreate):
    new_teacher = model.Teacher(
        user_id=data.user_id,
        age=data.age,
        sex=data.sex,
        experience=data.experience
    )
    db.add(new_teacher)
    await db.commit()
    await db.refresh(new_teacher)
    return new_teacher


async def get_teacher(db: AsyncSession, teacher_id: int):
    result = await db.execute(
        select(model.Teacher)
        .where(model.Teacher.id == teacher_id)
        .options(joinedload(model.Teacher.user))
    )
    return result.scalars().first()


# =========================================================
# CLASS CRUD
# =========================================================
async def create_class(db: AsyncSession, data: schemas.ClassCreate):
    new_class = model.Class(
        name=data.name,
        category=data.category
    )
    db.add(new_class)
    await db.commit()
    await db.refresh(new_class)
    return new_class


async def get_class(db: AsyncSession, class_id: int):
    result = await db.execute(select(model.Class).where(model.Class.id == class_id))
    return result.scalars().first()


async def get_all_classes(db: AsyncSession):
    result = await db.execute(select(model.Class))
    return result.scalars().all()


# =========================================================
# SUBJECT CRUD
# =========================================================
async def create_subject(db: AsyncSession, data: schemas.SubjectCreate):
    new_subject = model.Subject(name=data.name)
    db.add(new_subject)
    await db.commit()
    await db.refresh(new_subject)
    return new_subject


async def get_all_subjects(db: AsyncSession):
    result = await db.execute(select(model.Subject))
    return result.scalars().all()


# =========================================================
# CLASS ASSIGNMENT CRUD
# =========================================================
async def create_assignment(db: AsyncSession, data: schemas.ClassAssignmentCreate):
    new_assignment = model.ClassAssignment(
        teacher_id=data.teacher_id,
        class_id=data.class_id,
        subject_id=data.subject_id
    )
    db.add(new_assignment)
    await db.commit()
    await db.refresh(new_assignment)
    return new_assignment


async def get_teacher_assignments(db: AsyncSession, teacher_id: int):
    result = await db.execute(
        select(model.ClassAssignment).where(model.ClassAssignment.teacher_id == teacher_id)
    )
    return result.scalars().all()


# =========================================================
# MARKS CRUD
# =========================================================
async def add_marks(db: AsyncSession, data: schemas.MarksCreate):
    new_marks = model.Marks(
        student_id=data.student_id,
        subject_id=data.subject_id,
        teacher_id=data.teacher_id,
        score=data.score,
        date=data.date or date.today(),
    )
    db.add(new_marks)
    await db.commit()
    await db.refresh(new_marks)
    return new_marks


async def get_student_marks(db: AsyncSession, student_id: int):
    result = await db.execute(
        select(model.Marks).where(model.Marks.student_id == student_id)
    )
    return result.scalars().all()


# =========================================================
# ATTENDANCE CRUD
# =========================================================
async def mark_attendance(db: AsyncSession, data: schemas.AttendanceCreate):
    new_att = model.Attendance(
        student_id=data.student_id,
        teacher_id=data.teacher_id,
        subject_id=data.subject_id,
        status=data.status,
        date=data.date or date.today()
    )
    db.add(new_att)
    await db.commit()
    await db.refresh(new_att)
    return new_att


async def get_attendance(db: AsyncSession, student_id: int):
    result = await db.execute(
        select(model.Attendance).where(model.Attendance.student_id == student_id)
    )
    return result.scalars().all()


# =========================================================
# BEHAVIOR CRUD
# =========================================================
async def add_behavior(db: AsyncSession, data: schemas.BehaviorCreate):
    new_b = model.Behavior(
        student_id=data.student_id,
        teacher_id=data.teacher_id,
        remarks=data.remarks,
        date=data.date or date.today()
    )
    db.add(new_b)
    await db.commit()
    await db.refresh(new_b)
    return new_b


async def get_behavior(db: AsyncSession, student_id: int):
    result = await db.execute(
        select(model.Behavior).where(model.Behavior.student_id == student_id)
    )
    return result.scalars().all()


# =========================================================
# NOTIFICATIONS CRUD
# =========================================================
async def create_notification(db: AsyncSession, data: schemas.NotificationCreate):
    """Create notification for:
    - specific class
    - or ALL classes
    """
    new_notif = model.Notification(
        title=data.title,
        message=data.message,
        type=data.type,
        target_class_id=data.target_class_id,  # None = ALL
    )
    db.add(new_notif)
    await db.commit()
    await db.refresh(new_notif)
    return new_notif


async def get_notifications_for_user(db: AsyncSession, user: model.User):
    """If notification has a target class:
        - Only students of that class can see it
       Else:
        - Everyone sees
    """
    if user.role == "student":
        result = await db.execute(
            select(model.Notification)
            .join(model.Student, model.Student.class_id == model.Notification.target_class_id)
            .where(model.Student.user_id == user.id)
        )
        class_specific = result.scalars().all()

        result2 = await db.execute(
            select(model.Notification).where(model.Notification.target_class_id == None)
        )
        global_notifs = result2.scalars().all()

        return class_specific + global_notifs

    else:
        # teachers or admin see everything
        result = await db.execute(select(model.Notification))
        return result.scalars().all()
