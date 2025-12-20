import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# ---------------------------------------------------------
# LOAD ENV
# ---------------------------------------------------------
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is missing! Check your .env file.")

# ---------------------------------------------------------
# ENGINE + SESSION
# ---------------------------------------------------------
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

# ---------------------------------------------------------
# GET DB
# ---------------------------------------------------------
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
