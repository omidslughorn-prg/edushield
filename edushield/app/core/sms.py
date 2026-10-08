import os
import logging
from typing import Optional
from kavenegar import KavenegarAPI, APIException, HTTPException

# تنظیمات لوگ برای مشاهده پیامک‌های ارسالی در محیط توسعه
logger = logging.getLogger("sms_service")
logging.basicConfig(level=logging.INFO)

# دریافت کلید API کاوه‌نگار از فایل تنظیمات .env
KAVENEGAR_API_KEY = os.getenv("KAVENEGAR_API_KEY", "your_api_key_here")

class SMSService:
    """ سرویس ارسال پیامک اطلاع‌رسانی به اولیا """

    @staticmethod
    async def send_attendance_notification(
        mobile: str,
        student_name: str,
        status_text: str,
        record_date: str,
        entry_time: Optional[str] = None,
        delay_minutes: Optional[str] = None
    ) -> bool:
        """ ارسال پیامک اطلاع‌رسانی تاخیر/غیبت به ولی دانش‌آموز """

        # ۱. تنظیم متن پیامک
        if entry_time and delay_minutes and delay_minutes != "0":
            message = (
                f"ولی محترم، فرزند شما {student_name} در تاریخ {record_date} "
                f"ساعت {entry_time} با {delay_minutes} دقیقه تاخیر وارد مدرسه شد.\n"
                f"سامانه ناظم‌همراه"
            )
        else:
            message = (
                f"ولی محترم، وضعیت حضور فرزند شما {student_name} در تاریخ {record_date} "
                f"به صورت «{status_text}» ثبت گردید.\n"
                f"سامانه ناظم‌همراه"
            )

        # ۲. حالت شبیه‌سازی (وقتی کلید واقعی در .env تنظیم نشده است)
        if not KAVENEGAR_API_KEY or KAVENEGAR_API_KEY == "your_api_key_here":
            logger.info("=" * 60)
            logger.info(f"📲 [KAVENEGAR MOCK] To: {mobile}")
            logger.info(f"✉️ [MESSAGE]:\n{message}")
            logger.info("=" * 60)
            return True

        # ۳. حالت ارسال واقعی از طریق API کاوه‌نگار
        try:
            api = KavenegarAPI(KAVENEGAR_API_KEY)
            params = {
                'receptor': mobile,
                'message': message,
            }
            response = api.sms_send(params)
            logger.info(f"✅ پیامک واقعی با موفقیت ارسال شد: {response}")
            return True
        except (APIException, HTTPException) as e:
            logger.error(f"❌ خطای ارسال پیامک کاوه‌نگار: {e}")
            return False

sms_service = SMSService()