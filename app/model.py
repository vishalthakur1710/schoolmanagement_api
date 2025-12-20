from sqlalchemy import (
    Column, Integer, String, ForeignKey, Enum, Boolean, Date,
    Time, DateTime, UniqueConstraint, Index, Table
)
from sqlalchemy.orm import relationship, declarative_base
import enum
from datetime import datetime

Base = declarative_base()


# =========================================================
# ENUMS
# =========================================================

class UserRole(str, enum.Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"


class SexEnum(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"


class AttendanceStatus(str, enum.Enum):
    present = "Present"
    absent = "Absent"


class DayEnum(str, enum.Enum):
    mon = "Mon"
    tue = "Tue"
    wed = "Wed"
    thu = "Thu"
    fri = "Fri"
    sat = "Sat"
    sun = "Sun"


class NotificationType(str, enum.Enum):
    new_student = "new_student"
    message = "message"
    class_message = "class_message"   # NEW (for specific class)
    global_message = "global_message" # NEW (for everyone)


# =========================================================
# USER
# =========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student_profile = relationship("Student", back_populates="user", uselist=False)
    teacher_profile = relationship("Teacher", back_populates="user", uselist=False)
    notifications = relationship("NotificationRecipient", back_populates="user")


# =========================================================
# CLASS (UPDATED)
# =========================================================

class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)  
    # Example of values:
    # Class 1, Class 10, Class 11 Arts, Class 12 Commerce etc.

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    students = relationship("Student", back_populates="class_")
    assignments = relationship("ClassAssignment", back_populates="class_")
    notifications = relationship("Notification", back_populates="class_")

    __table_args__ = (Index("idx_class_name", "name"),)


# =========================================================
# SUBJECT
# =========================================================

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assignments = relationship("ClassAssignment", back_populates="subject")


# =========================================================
# TEACHER-SUBJECT JUNCTION
# =========================================================

teacher_subject_table = Table(
    "teacher_subject",
    Base.metadata,
    Column("teacher_id", Integer, ForeignKey("teachers.id"), primary_key=True),
    Column("subject_id", Integer, ForeignKey("subjects.id"), primary_key=True)
)


# =========================================================
# STUDENT
# =========================================================

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    class_id = Column(Integer, ForeignKey("classes.id"))

    age = Column(Integer)
    sex = Column(Enum(SexEnum))
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="student_profile")
    class_ = relationship("Class", back_populates="students")
    marks = relationship("Marks", back_populates="student")
    attendance = relationship("Attendance", back_populates="student")
    behavior = relationship("Behavior", back_populates="student")


# =========================================================
# TEACHER
# =========================================================

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    age = Column(Integer)
    sex = Column(Enum(SexEnum))
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="teacher_profile")
    subjects = relationship("Subject", secondary=teacher_subject_table, backref="teachers")
    assignments = relationship("ClassAssignment", back_populates="teacher")
    marks = relationship("Marks", back_populates="teacher")
    attendance = relationship("Attendance", back_populates="teacher")
    behavior = relationship("Behavior", back_populates="teacher")


# =========================================================
# SCHEDULE
# =========================================================

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Enum(DayEnum), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assignment_schedules = relationship("AssignmentSchedule", back_populates="schedule")


# =========================================================
# CLASS ASSIGNMENT
# =========================================================

class ClassAssignment(Base):
    __tablename__ = "class_assignments"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    teacher = relationship("Teacher", back_populates="assignments")
    class_ = relationship("Class", back_populates="assignments")
    subject = relationship("Subject", back_populates="assignments")
    schedules = relationship("AssignmentSchedule", back_populates="assignment")


# =========================================================
# ASSIGNMENT SCHEDULE
# =========================================================

class AssignmentSchedule(Base):
    __tablename__ = "assignment_schedules"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("class_assignments.id"))
    schedule_id = Column(Integer, ForeignKey("schedules.id"))
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assignment = relationship("ClassAssignment", back_populates="schedules")
    schedule = relationship("Schedule", back_populates="assignment_schedules")


# =========================================================
# MARKS
# =========================================================

class Marks(Base):
    __tablename__ = "marks"
    __table_args__ = (
        UniqueConstraint("student_id", "subject_id", "date", name="unique_student_subject_date"),
    )

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    score = Column(Integer)
    date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("Student", back_populates="marks")
    teacher = relationship("Teacher", back_populates="marks")


# =========================================================
# ATTENDANCE
# =========================================================

class Attendance(Base):
    __tablename__ = "attendance"
    __table_args__ = (
        UniqueConstraint("student_id", "subject_id", "date", name="unique_attendance"),
    )

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    status = Column(Enum(AttendanceStatus), nullable=False)
    date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("Student", back_populates="attendance")
    teacher = relationship("Teacher", back_populates="attendance")


# =========================================================
# BEHAVIOR
# =========================================================

class Behavior(Base):
    __tablename__ = "behavior"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    remarks = Column(String(500))
    date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("Student", back_populates="behavior")
    teacher = relationship("Teacher", back_populates="behavior")


# =========================================================
# NOTIFICATIONS (UPDATED)
# =========================================================

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    message = Column(String(1000))
    type = Column(Enum(NotificationType))

    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)
    # null → global message
    # class_id → message for specific class

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class_ = relationship("Class", back_populates="notifications")
    recipients = relationship("NotificationRecipient", back_populates="notification")


# =========================================================
# NOTIFICATION RECIPIENT
# =========================================================

class NotificationRecipient(Base):
    __tablename__ = "notification_recipients"

    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(Integer, ForeignKey("notifications.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    is_read = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    notification = relationship("Notification", back_populates="recipients")
    user = relationship("User", back_populates="notifications")
