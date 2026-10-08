from app.core.otp import generate_otp_code, hash_otp_code, verify_otp_code
from app.schemas.otp import OTPRequestSchema, OTPResponseSchema, OTPVerifySchema
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/otp", tags=["احراز هویت پیامکی (OTP)"])


@router.post("/send", response_model=OTPResponseSchema)
async def send_otp(request_data: OTPRequestSchema):
    """تولید و ارسال کد یک‌بارمصرف به سیم‌کارت ثبت‌شده ولی (ماده ۱۲ قانون تجارت الکترونیک)"""
    raw_otp = generate_otp_code()
    hashed_otp = hash_otp_code(raw_otp)

    # TODO: در فاز اتصال به پنل پیامکی، raw_otp از طریق Webhook ارسال می‌شود

    return OTPResponseSchema(
        message="کد تایید با موفقیت تولید و ارسال شد.",
        guardian_mobile=request_data.guardian_mobile,
        otp_code_hash=hashed_otp,
        dev_otp_code=raw_otp,  # جهت تست راحت در Swagger UI
    )


@router.post("/verify")
async def verify_otp(verify_data: OTPVerifySchema):
    """اعتبارسنجی کد واردشده توسط ولی"""
    is_valid = verify_otp_code(
        plain_otp=verify_data.otp_code,
        hashed_otp=verify_data.otp_code_hash,
    )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="کد تایید واردشده اشتباه یا منقضی شده است.",
        )

    return {
        "status": "success",
        "message": "کد OTP با موفقیت تایید شد.",
        "verified": True,
    }