import hashlib
import json
from datetime import datetime


def generate_legal_transaction_hash(
    transaction_id: str,
    student_id: str,
    guardian_national_id: str,
    guardian_mobile: str,
    reason: str,
    timestamp_utc: datetime,
    otp_code_hash: str,
    signature_vector: str,
) -> str:
    """تولید هش SHA-256 از تمام داده‌های تراکنش مرخصی جهت قفل رمزنگاری‌شده و اثبات اصالت در دادگاه (ماده ۱۵ قانون تجارت الکترونیک)"""
    payload = {
        "transaction_id": transaction_id,
        "student_id": student_id,
        "guardian_national_id": guardian_national_id,
        "guardian_mobile": guardian_mobile,
        "reason": reason,
        "timestamp_utc": timestamp_utc.isoformat(),
        "otp_code_hash": otp_code_hash,
        "signature_vector": signature_vector,
    }

    # تبدیل دیکشنری به رشته استاندارد JSON با ترتیب ثابت کلیدها جهت یکسان بودن هش
    payload_string = json.dumps(payload, sort_keys=True)

    # تولید هش SHA-256
    return hashlib.sha256(payload_string.encode("utf-8")).hexdigest()
