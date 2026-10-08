import app.db.models
from app.db.seed import seed_initial_data
from app.db.session import Base, engine


async def init_db():
    async with engine.begin() as conn:
        # ساخت جدول‌ها در صورت عدم وجود
        await conn.run_sync(Base.metadata.create_all)

    # درج داده‌های نمونه اولیه
    await seed_initial_data()