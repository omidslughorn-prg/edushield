from app.db.models import ClassRoom, School, Student
from app.db.session import AsyncSessionLocal


async def seed_initial_data():
    """درج مدرسه، کلاس و دانش‌آموز نمونه جهت تست و ساختار Multi-Tenant"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # ۱. ایجاد یا دریافت مدرسه نمونه
            sample_school = await session.get(School, 1)
            if not sample_school:
                sample_school = School(
                    id=1,
                    name="دبستان شهید همت (نمونه)",
                    code="SCH-1001",
                    is_active=True,
                )
                session.add(sample_school)
                await session.flush()  # اطمینان از ثبت ID مدرسه

            # ۲. ایجاد کلاس نمونه با school_id
            existing_class = await session.get(ClassRoom, "CLS-601")
            if not existing_class:
                sample_class = ClassRoom(
                    id="CLS-601",
                    school_id=sample_school.id,
                    name="پایه ششم - کلاس الف",
                    grade="ششم",
                )
                session.add(sample_class)

            # ۳. ایجاد دانش‌آموز نمونه با school_id
            existing_student = await session.get(Student, "STU-980124")
            if not existing_student:
                sample_student = Student(
                    id="STU-980124",
                    school_id=sample_school.id,
                    national_id="0012345678",
                    first_name="علی",
                    last_name="علوی",
                    class_id="CLS-601",
                    guardian_name="محمد علوی",
                    guardian_mobile="09123456789",
                )
                session.add(sample_student)