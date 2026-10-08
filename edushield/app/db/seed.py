from app.db.models import ClassRoom, Student
from app.db.session import AsyncSessionLocal


async def seed_initial_data():
    """درج کلاس و دانش‌آموز نمونه جهت تست ثبت مرخصی اضطراری"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # بررسی وجود کلاس نمونه
            existing_class = await session.get(ClassRoom, "CLS-601")
            if not existing_class:
                sample_class = ClassRoom(
                    id="CLS-601",
                    name="پایه ششم - کلاس الف",
                    grade="ششم",
                )
                session.add(sample_class)

            # بررسی وجود دانش‌آموز نمونه
            existing_student = await session.get(Student, "STU-980124")
            if not existing_student:
                sample_student = Student(
                    id="STU-980124",
                    national_id="0012345678",
                    first_name="علی",
                    last_name="علوی",
                    class_id="CLS-601",
                    guardian_name="محمد علوی",
                    guardian_mobile="09123456789",
                )
                session.add(sample_student)