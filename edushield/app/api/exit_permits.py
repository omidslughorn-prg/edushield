from app.core.security import generate_legal_transaction_hash
from app.db.models import ExitPermit, Student
from app.db.session import get_db
from app.schemas.legal import LegalExitTransactionSchema
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/exit-permits", tags=["مرخصی اضطراری و سپر حقوقی"])


@router.post(
    "/create",
    response_model=LegalExitTransactionSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_exit_permit(
    permit_data: LegalExitTransactionSchema,
    db: AsyncSession = Depends(get_db),
):
    # ۱. بررسی وجود دانش‌آموز در دیتابیس
    student = await db.get(Student, permit_data.student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"دانش‌آموزی با شناسه {permit_data.student_id} یافت نشد.",
        )

    # ۲. محاسبه و قفل رمزنگاری هش SHA-256
    calculated_hash = generate_legal_transaction_hash(
        transaction_id=permit_data.transaction_id,
        student_id=permit_data.student_id,
        guardian_national_id=permit_data.guardian_national_id,
        guardian_mobile=permit_data.guardian_mobile,
        reason=permit_data.reason,
        timestamp_utc=permit_data.timestamp_utc,
        otp_code_hash=permit_data.otp_code_hash,
        signature_vector=permit_data.signature_vector,
    )

    permit_data.digital_signature_hash = calculated_hash

    # ۳. ساخت مدل دیتابیس و ذخیره‌سازی دائمی
    db_exit_permit = ExitPermit(
        transaction_id=permit_data.transaction_id,
        student_id=permit_data.student_id,
        guardian_national_id=permit_data.guardian_national_id,
        guardian_mobile=permit_data.guardian_mobile,
        receiver_relationship=permit_data.receiver_relationship,
        reason=permit_data.reason,
        timestamp_utc=permit_data.timestamp_utc,
        otp_code_hash=permit_data.otp_code_hash,
        signature_vector=permit_data.signature_vector,
        digital_signature_hash=calculated_hash,
    )

    db.add(db_exit_permit)
    await db.commit()
    await db.refresh(db_exit_permit)

    return permit_data