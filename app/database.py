import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# ---------------------------------------------------------
# LOAD CORRECT ENV FILE
# ---------------------------------------------------------
ENV = os.getenv("ENV", "local")

if ENV == "docker":
    load_dotenv(".env.docker")
else:
    load_dotenv(".env")

# ---------------------------------------------------------
# DATABASE URL
# ---------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL is missing! Check your env file.")

# ---------------------------------------------------------
# SQLALCHEMY BASE (models)
# ---------------------------------------------------------
from app.model import Base as ModelBase
Base = ModelBase

# ---------------------------------------------------------
# ENGINE + SESSION
# ---------------------------------------------------------
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# ---------------------------------------------------------
# DEPENDENCY
# ---------------------------------------------------------
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
