from pydantic import BaseModel, ConfigDict, Field
from datetime import date, time
from typing import Optional
from app.db.models import AttendanceStatus

class AttendanceCreateSchema(BaseModel):
    student_id: str = Field(..., example="STU-980124")
    record_date: date = Field(default_factory=date.today)
    entry_time: Optional[time] = Field(None, example="07:50:00")
    delay_minutes: Optional[int] = Field(0, example=20)
    status: AttendanceStatus = Field(..., example=AttendanceStatus.LATE)
    description: Optional[str] = Field(None, example="گیر کردن در ترافیک")

class AttendanceResponseSchema(BaseModel):
    id: str
    student_id: str
    record_date: date
    entry_time: Optional[time]
    delay_minutes: Optional[int]
    status: AttendanceStatus
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)