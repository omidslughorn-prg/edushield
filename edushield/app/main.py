from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.exit_permits import router as exit_permits_router
from app.api.otp import router as otp_router
from app.api.attendance import router as attendance_router
from app.api.reports import router as reports_router
from app.db.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="EduShield API",
    description="سامانه مدیریت انضباطی، مرخصی اضطراری و سپر حقوقی مدارس",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# اتصال مسیرها
app.include_router(exit_permits_router)
app.include_router(otp_router)
app.include_router(attendance_router)
app.include_router(reports_router)

@app.get("/", tags=["Health Check"])
async def root():
    return {"status": "online", "system": "EduShield API"}

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy"}