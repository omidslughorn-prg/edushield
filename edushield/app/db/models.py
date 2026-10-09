from datetime import date, datetime, time
from enum import Enum
from app.db.session import Base
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
)
from sqlalchemy.orm import relationship


# انوم وضعیت حضور و غیاب برای سازگاری با api و schemas
class AttendanceStatus(str, Enum):
    PRESENT = "present"  # حاضر
    LATE = "late"  # تاخیر ورود
    EXCUSED_ABSENCE = "excused"  # غیبت موجه
    UNEXCUSED_ABSENCE = "unexcused"  # غیبت غیرموجه


# ۱. مدل مدارس (Tenants)
class School(Base):
    """مدل مدارس (پشتیبانی از Multi-Tenant)"""

    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)  # نام مدرسه
    code = Column(String(50), unique=True, index=True, nullable=False)  # کد اختصاصی
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # ارتباطات
    users = relationship("User", back_populates="school")
    classes = relationship("ClassRoom", back_populates="school")
    students = relationship("Student", back_populates="school")
    attendance_records = relationship("AttendanceRecord", back_populates="school")
    exit_permits = relationship("ExitPermit", back_populates="school")


# ۲. مدل کاربران / ناظم‌ها / مدیران مدارس
class User(Base):
    """مدل کاربران و ناظم‌های مدارس"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    role = Column(String(50), default="vice_principal")  # vice_principal, admin

    school = relationship("School", back_populates="users")


# ۳. مدل کلاس‌ها
class ClassRoom(Base):
    """مدل کلاس‌های درس مدرسه"""

    __tablename__ = "classes"

    id = Column(String, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    grade = Column(String(50), nullable=False)

    school = relationship("School", back_populates="classes")
    students = relationship("Student", back_populates="classroom")


# ۴. مدل دانش‌آموزان
class Student(Base):
    """مدل دانش‌آموزان"""

    __tablename__ = "students"

    id = Column(String, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    national_id = Column(String(10), index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    class_id = Column(String, ForeignKey("classes.id"), nullable=False)

    guardian_name = Column(String(100), nullable=False)
    guardian_mobile = Column(String(11), nullable=False, index=True)

    school = relationship("School", back_populates="students")
    classroom = relationship("ClassRoom", back_populates="students")
    exit_permits = relationship("ExitPermit", back_populates="student")
    attendance_records = relationship("AttendanceRecord", back_populates="student")


# ۵. مدل حضور و غیاب
class AttendanceRecord(Base):
    """مدل ثبت حضور و غیاب روزانه"""

    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    record_date = Column(Date, default=date.today, nullable=False, index=True)
    entry_time = Column(Time, nullable=True)
    delay_minutes = Column(Integer, default=0)
    status = Column(SQLEnum(AttendanceStatus), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    school = relationship("School", back_populates="attendance_records")
    student = relationship("Student", back_populates="attendance_records")


# ۶. مدل مرخصی اضطراری و لاگ‌های حقوقی (سپر حقوقی)
class ExitPermit(Base):
    """مدل مجوزهای خروج اضطراری و لاگ‌های حقوقی"""

    __tablename__ = "exit_permits"

    transaction_id = Column(String, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    guardian_national_id = Column(String(10), nullable=False)
    guardian_mobile = Column(String(11), nullable=False)
    receiver_relationship = Column(String(50), nullable=False)
    reason = Column(Text, nullable=False)
    timestamp_utc = Column(DateTime, default=datetime.utcnow, nullable=False)
    otp_code_hash = Column(String, nullable=False)
    signature_vector = Column(Text, nullable=False)
    digital_signature_hash = Column(String, nullable=False, unique=True)

    school = relationship("School", back_populates="exit_permits")
    student = relationship("Student", back_populates="exit_permits")