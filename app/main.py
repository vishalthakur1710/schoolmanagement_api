from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine, get_db
from app.model import Base
from app.router import auth, admin, students, teachers, notifications

import asyncio

# =========================================================
# APP INIT
# =========================================================
app = FastAPI(
    title="School Management API",
    description="Async FastAPI backend for managing students, teachers, classes, marks, attendance, behavior, and notifications",
    version="1.0.0"
)

# =========================================================
# CORS (if needed)
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# INCLUDE ROUTERS
# =========================================================
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(notifications.router)


# =========================================================
# STARTUP EVENT: CREATE ALL TABLES
# =========================================================
@app.on_event("startup")
async def startup():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Database tables created")
    except SQLAlchemyError as e:
        print(f"❌ Database startup error: {e}")


# =========================================================
# SHUTDOWN EVENT
# =========================================================
@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
    print(" Database connection closed")


# =========================================================
# SIMPLE ROOT ENDPOINT
# =========================================================
@app.get("/")
async def root():
    return {"message": "Welcome to School Management API!"}
