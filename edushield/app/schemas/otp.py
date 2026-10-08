from pydantic import BaseModel, ConfigDict, Field


class OTPRequestSchema(BaseModel):
    guardian_mobile: str = Field(
        ..., pattern=r"^09\d{9}$", example="09123456789"
    )
    student_id: str = Field(..., example="STU-980124")


class OTPVerifySchema(BaseModel):
    guardian_mobile: str = Field(
        ..., pattern=r"^09\d{9}$", example="09123456789"
    )
    otp_code: str = Field(
        ..., min_length=6, max_length=6, example="123456"
    )
    otp_code_hash: str = Field(
        ..., description="هش دریافت‌شده در مرحله درخواست OTP"
    )


class OTPResponseSchema(BaseModel):
    message: str
    guardian_mobile: str
    otp_code_hash: str
    # در محیط واقعی کد پیامک می‌شود، اما برای تست در فاز توسعه کد خام نیز برگردانده می‌شود
    dev_otp_code: str | None = None

    model_config = ConfigDict(from_attributes=True)