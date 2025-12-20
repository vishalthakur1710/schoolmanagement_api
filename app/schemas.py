from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, time, datetime
from enum import Enum


# ===========================
# ENUMS
# ===========================
class UserRole(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"


class SexEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class AttendanceStatus(str, Enum):
    present = "Present"
    absent = "Absent"


class DayEnum(str, Enum):
    mon = "Mon"
    tue = "Tue"
    wed = "Wed"
    thu = "Thu"
    fri = "Fri"
    sat = "Sat"
    sun = "Sun"


class NotificationType(str, Enum):
    new_student = "new_student"
    message = "message"


# ===========================
# USER SCHEMAS
# ===========================
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ===========================
# CLASS SCHEMAS
# ===========================
class ClassBase(BaseModel):
    name: str


class ClassCreate(ClassBase):
    pass


class ClassRead(ClassBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ===========================
# SUBJECT SCHEMAS
# ===========================
class SubjectBase(BaseModel):
    name: str


class SubjectCreate(SubjectBase):
    pass


class SubjectRead(SubjectBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ===========================
# STUDENT SCHEMAS
# ===========================
class StudentBase(BaseModel):
    age: Optional[int] = None
    sex: Optional[SexEnum] = None
    class_id: Optional[int] = None


class StudentCreate(StudentBase):
    user_id: int


class StudentUpdate(StudentBase):
    pass


class StudentRead(StudentBase):
    id: int
    user: UserRead
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ===========================
# TEACHER SCHEMAS
# ===========================
class TeacherBase(BaseModel):
    age: Optional[int] = None
    sex: Optional[SexEnum] = None


class TeacherCreate(TeacherBase):
    user_id: int
    subject_ids: Optional[List[int]] = None  # FIXED


class TeacherUpdate(TeacherBase):
    subject_ids: Optional[List[int]] = None  # FIXED


class TeacherRead(TeacherBase):
    id: int
    user: UserRead
    subjects: Optional[List[SubjectRead]] = None  # FIXED
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ===========================
# SCHEDULE SCHEMAS
# ===========================
class ScheduleBase(BaseModel):
    day: DayEnum
    start_time: time
    end_time: time


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleRead(ScheduleBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ===========================
# CLASS ASSIGNMENT SCHEMAS
# ===========================
class ClassAssignmentBase(BaseModel):
    teacher_id: int
    class_id: int
    subject_id: int


class ClassAssignmentCreate(ClassAssignmentBase):
    pass


class ClassAssignmentRead(ClassAssignmentBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ===========================
# ASSIGNMENT SCHEDULE SCHEMAS
# ===========================
class AssignmentScheduleBase(BaseModel):
    assignment_id: int
    schedule_id: int


class AssignmentScheduleCreate(AssignmentScheduleBase):
    pass


class AssignmentScheduleRead(AssignmentScheduleBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ===========================
# MARKS SCHEMAS
# ===========================
class MarksBase(BaseModel):
    student_id: int
    subject_id: int
    teacher_id: int
    score: int
    date: date


class MarksCreate(MarksBase):
    pass


class MarksRead(MarksBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ===========================
# ATTENDANCE SCHEMAS
# ===========================
class AttendanceBase(BaseModel):
    student_id: int
    teacher_id: int
    subject_id: int
    status: AttendanceStatus
    date: date


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceRead(AttendanceBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ===========================
# BEHAVIOR SCHEMAS
# ===========================
class BehaviorBase(BaseModel):
    student_id: int
    teacher_id: int
    remarks: str
    date: date


class BehaviorCreate(BehaviorBase):
    pass


class BehaviorRead(BehaviorBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ===========================
# NOTIFICATION SCHEMAS
# ===========================
class NotificationBase(BaseModel):
    title: str
    message: str
    type: NotificationType


class NotificationCreate(NotificationBase):
    recipient_ids: List[int]


class NotificationRead(NotificationBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    recipients: List[int]

    model_config = {"from_attributes": True}


# ===========================
# NOTIFICATION RECIPIENT SCHEMAS
# ===========================
class NotificationRecipientRead(BaseModel):
    id: int
    notification_id: int
    user_id: int
    is_read: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
