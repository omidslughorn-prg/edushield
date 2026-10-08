from datetime import date, datetime, time
from enum import Enum
from app.db.session import Base
from sqlalchemy import Column, Date, DateTime, Enum as SQLEnum, ForeignKey, String, Text, Time
from sqlalchemy.orm import relationship

class ClassRoom(Base):
    """مدل کلاس‌های درس مدرسه (مثال: پایه ششم - کلاس الف)"""

    __tablename__ = "classes"

    id = Column(String, primary_key=True, index=True)  # مثل: CLS-601
    name = Column(String(100), nullable=False)  # مثل: پایه ششم - کلاس الف
    grade = Column(String(50), nullable=False)  # مثل: ششم

    # ارتباط یک‌به‌چند با دانش‌آموزان
    students = relationship("Student", back_populates="classroom")


class Student(Base):
    """مدل دانش‌آموزان"""

    __tablename__ = "students"

    id = Column(String, primary_key=True, index=True)  # مثل: STU-980124
    national_id = Column(String(10), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    class_id = Column(String, ForeignKey("classes.id"), nullable=False)

    # اطلاعات ولی قانونی
    guardian_name = Column(String(100), nullable=False)
    guardian_mobile = Column(String(11), nullable=False, index=True)

    # ارتباطات
    classroom = relationship("ClassRoom", back_populates="students")
    exit_permits = relationship("ExitPermit", back_populates="student")
    attendance_records = relationship("AttendanceRecord", back_populates="student")

class ExitPermit(Base):
    """مدل مجوزهای خروج اضطراری و لاگ‌های حقوقی (سپر حقوقی)"""

    __tablename__ = "exit_permits"

    transaction_id = Column(
        String, primary_key=True, index=True
    )  # مثل: REQ-20261002-8841
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    guardian_national_id = Column(String(10), nullable=False)
    guardian_mobile = Column(String(11), nullable=False)
    receiver_relationship = Column(String(50), nullable=False)
    reason = Column(Text, nullable=False)
    timestamp_utc = Column(DateTime, default=datetime.utcnow, nullable=False)
    otp_code_hash = Column(String, nullable=False)
    signature_vector = Column(Text, nullable=False)
    digital_signature_hash = Column(String, nullable=False, unique=True)

    # ارتباط با دانش‌آموز
    student = relationship("Student", back_populates="exit_permits")

class AttendanceStatus(str, Enum):
    PRESENT = "present"            # حاضر
    LATE = "late"                  # تاخیر ورود
    EXCUSED_ABSENCE = "excused"    # غیبت موجه
    UNEXCUSED_ABSENCE = "unexcused"# غیبت غیرموجه

class AttendanceRecord(Base):
    """مدل ثبت ورود، تاخیر و غیبت دانش‌آموزان در حیاط/کلاس"""
    __tablename__ = "attendance_records"

    id = Column(String, primary_key=True, index=True) # مثل: ATT-20261005-980124
    student_id = Column(String, ForeignKey("students.id"), nullable=False, index=True)
    record_date = Column(Date, default=date.today, nullable=False, index=True)
    entry_time = Column(Time, nullable=True) # زمان دقیق ورود در صورت تاخیر
    delay_minutes = Column(String, nullable=True) # میزان تاخیر به دقیقه
    status = Column(SQLEnum(AttendanceStatus), nullable=False)
    description = Column(Text, nullable=True) # توضیحات یا علت تاخیر

    # ارتباط با دانش‌آموز
    student = relationship("Student", back_populates="attendance_records")