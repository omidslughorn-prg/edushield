import io
import pandas as pd
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import AttendanceRecord, Student, ClassRoom

class ExcelExportService:
    """سرویس تولید گزارش‌های اکسل جهت سامانه سیدا و بایگانی مدرسه"""

    @staticmethod
    async def generate_attendance_excel(
        db: AsyncSession, 
        start_date: date, 
        end_date: date
    ) -> io.BytesIO:
        """استخراج گزارش تاخیرها و غیبت‌ها در بازه زمانی مشخص به فرمت اکسل"""
        
        # ۱. کوئری دریافت اطلاعات حضور/غیبت به همراه اطلاعات دانش‌آموز و کلاس
        query = (
            select(
                AttendanceRecord.record_date,
                Student.national_id,
                Student.first_name,
                Student.last_name,
                ClassRoom.name.label("class_name"),
                AttendanceRecord.status,
                AttendanceRecord.entry_time,
                AttendanceRecord.delay_minutes,
                AttendanceRecord.description
            )
            .join(Student, AttendanceRecord.student_id == Student.id)
            .join(ClassRoom, Student.class_id == ClassRoom.id)
            .where(AttendanceRecord.record_date.between(start_date, end_date))
            .order_by(AttendanceRecord.record_date.desc())
        )

        result = await db.execute(query)
        rows = result.all()

        # ۲. تبدیل داده‌ها به لیست دیکشنری جهت بارگذاری در Pandas
        data_list = []
        status_farsi = {
            "present": "حاضر",
            "late": "تاخیر ورود",
            "excused": "غیبت موجه",
            "unexcused": "غیبت غیرموجه"
        }

        for row in rows:
            data_list.append({
                "تاریخ ثبت": str(row.record_date),
                "کد ملی دانش‌آموز": row.national_id,
                "نام": row.first_name,
                "نام خانوادگی": row.last_name,
                "کلاس": row.class_name,
                "وضعیت حضور": status_farsi.get(row.status.value, str(row.status)),
                "زمان ورود": str(row.entry_time) if row.entry_time else "-",
                "میزان تاخیر (دقیقه)": row.delay_minutes if row.delay_minutes else "0",
                "توضیحات / علت": row.description if row.description else "-"
            })

        # ۳. ساخت DataFrame با Pandas
        df = pd.DataFrame(data_list)

        # اگر داده‌ای در این بازه وجود نداشت، یک جدول خالی با ستون‌ها می‌سازد
        if df.empty:
            df = pd.DataFrame(columns=[
                "تاریخ ثبت", "کد ملی دانش‌آموز", "نام", "نام خانوادگی",
                "کلاس", "وضعیت حضور", "زمان ورود", "میزان تاخیر (دقیقه)", "توضیحات / علت"
            ])

        # ۴. ذخیره در حافظه رم (BytesIO) به جای ذخیره روی دیسک
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='گزارش_حضور_غیبت')

        output.seek(0)
        return output

export_service = ExcelExportService()