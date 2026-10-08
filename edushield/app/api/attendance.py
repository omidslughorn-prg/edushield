import uuid
from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models import AttendanceRecord, Student, AttendanceStatus
from app.schemas.attendance import AttendanceCreateSchema, AttendanceResponseSchema
from app.core.sms import sms_service

router = APIRouter(prefix="/attendance", tags=["مدیریت تاخیر و غیبت حیاط/صف"])

# دیکشنری ترجمه وضعیت‌ها به فارسی جهت درج در پیامک
STATUS_TRANSLATIONS = {
    AttendanceStatus.PRESENT: "حاضر",
    AttendanceStatus.LATE: "تاخیر ورود",
    AttendanceStatus.EXCUSED_ABSENCE: "غیبت موجه",
    AttendanceStatus.UNEXCUSED_ABSENCE: "غیبت غیرموجه",
}

@router.post("/record", response_model=AttendanceResponseSchema, status_code=status.HTTP_201_CREATED)
async def record_attendance(
    data: AttendanceCreateSchema,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """ثبت سریع تاخیر یا غیبت دانش‌آموز به همراه ارسال پیامک خودکار به ولی"""
    
    # ۱. بررسی وجود دانش‌آموز
    student = await db.get(Student, data.student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"دانش‌آموزی با شناسه {data.student_id} یافت نشد."
        )

    # ۲. ایجاد رکورد حضور و غیاب در دیتابیس
    record_id = f"ATT-{date.today().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
    
    db_record = AttendanceRecord(
        id=record_id,
        student_id=data.student_id,
        record_date=data.record_date,
        entry_time=data.entry_time,
        delay_minutes=str(data.delay_minutes) if data.delay_minutes is not None else None,
        status=data.status,
        description=data.description
    )

    db.add(db_record)
    await db.commit()
    await db.refresh(db_record)

    # ۳. افزودن وظیفه ارسال پیامک به BackgroundTasks (بدون معطل کردن کاربر)
    if student.guardian_mobile:
        student_fullname = f"{student.first_name} {student.last_name}"
        status_text = STATUS_TRANSLATIONS.get(data.status, "ثبت شده")
        time_str = data.entry_time.strftime("%H:%M") if data.entry_time else None

        background_tasks.add_task(
            sms_service.send_attendance_notification,
            mobile=student.guardian_mobile,
            student_name=student_fullname,
            status_text=status_text,
            record_date=str(data.record_date),
            entry_time=time_str,
            delay_minutes=str(data.delay_minutes) if data.delay_minutes else None
        )

    return db_record


@router.get("/today", response_model=List[AttendanceResponseSchema])
async def get_today_records(db: AsyncSession = Depends(get_db)):
    """دریافت لیست تمام تاخیرها و غیبت‌های ثبت‌شده امروز"""
    today = date.today()
    result = await db.execute(
        select(AttendanceRecord).where(AttendanceRecord.record_date == today)
    )
    records = result.scalars().all()
    return records