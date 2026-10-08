import hashlib
import random
import string


def generate_otp_code(length: int = 6) -> str:
    """تولید یک کد OTP ۶ رقمی عددی"""
    return "".join(random.choices(string.digits, k=length))


def hash_otp_code(otp_code: str) -> str:
    """هش‌سازی کد OTP جهت ذخیره یا مقایسه امن در دیتابیس (عدم ذخیره کد متنی)"""
    return hashlib.sha256(otp_code.encode("utf-8")).hexdigest()


def verify_otp_code(plain_otp: str, hashed_otp: str) -> bool:
    """اعتبارسنجی کد واردشده توسط ولی با هش ذخیره‌شده"""
    return hash_otp_code(plain_otp) == hashed_otp