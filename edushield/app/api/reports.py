from datetime import date
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.export_service import export_service

router = APIRouter(prefix="/reports", tags=["گزارش‌گیری و خروجی اکسل"])

@router.get("/excel/attendance")
async def download_attendance_report(
    start_date: date = Query(default=date.today(), description="تاریخ شروع بازه (YYYY-MM-DD)"),
    end_date: date = Query(default=date.today(), description="تاریخ پایان بازه (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_db)
):
    """دانلود فایل اکسل تاخیرها و غیبت‌ها جهت بایگانی و واردسازی در سامانه سیدا"""
    
    excel_file = await export_service.generate_attendance_excel(db, start_date, end_date)
    
    filename = f"Attendance_Report_{start_date}_to_{end_date}.xlsx"
    
    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }

    return StreamingResponse(
        excel_file,
        headers=headers,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )