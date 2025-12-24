import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError

from app.database import engine
from app.model import Base
from app.routers import auth, admin, students, teachers, notifications

# =========================================================
# APP INIT (ONLY ONCE)
# =========================================================
app = FastAPI(
    title="School Management API",
    description="Async FastAPI backend for managing students, teachers, classes, marks, attendance, behavior, and notifications",
    version="1.0.0"
)

# =========================================================
# CORS
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# ROUTERS
# =========================================================
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(teachers.router, prefix="/teachers", tags=["Teachers"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])

# =========================================================
# STARTUP: WAIT FOR DB + CREATE TABLES
# =========================================================
@app.on_event("startup")
async def startup():
    max_retries = 20
    delay = 2  # seconds

    for attempt in range(1, max_retries + 1):
        try:
            async with engine.begin() as conn:
                # DEV ONLY (remove in prod, use Alembic)
                await conn.run_sync(Base.metadata.create_all)

                print("✅ Database connected & tables ready")
                return
        except OperationalError:
            print(f"⏳ Database not ready (attempt {attempt}/{max_retries})")
            await asyncio.sleep(delay)

    raise RuntimeError("❌ Database never became available")

# =========================================================
# SHUTDOWN
# =========================================================
@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
    print("🔌 Database connection closed")

# =========================================================
# ROOT
# =========================================================
@app.get("/")
async def root():
    return {"message": "Welcome to School Management API!"}
