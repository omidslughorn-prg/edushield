from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class LegalExitTransactionSchema(BaseModel):
    transaction_id: str = Field(..., example="REQ-20261002-8841")
    student_id: str = Field(..., example="STU-980124")
    guardian_national_id: str = Field(
        ..., min_length=10, max_length=10, example="0012345678"
    )
    guardian_mobile: str = Field(
        ..., pattern=r"^09\d{9}$", example="09123456789"
    )
    receiver_relationship: str = Field(..., example="پدر")
    reason: str = Field(..., example="مراجعه به پزشک")
    timestamp_utc: datetime
    otp_code_hash: str
    signature_vector: str
    digital_signature_hash: str = Field(
        ..., description="هش SHA-256 کل ساختار جهت جلوگیری از دستکاری"
    )

    model_config = ConfigDict(from_attributes=True)
    