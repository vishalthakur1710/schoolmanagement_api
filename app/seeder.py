
import asyncio
from sqlalchemy import select

from app.database import engine, AsyncSessionLocal, Base
from app import crud, schemas, models


CLASS_LIST = [
    *[f"Class {i}" for i in range(1, 11)],
    "Class 11 - Arts", "Class 11 - Commerce", "Class 11 - Medical", "Class 11 - Non-Medical",
    "Class 12 - Arts", "Class 12 - Commerce", "Class 12 - Medical", "Class 12 - Non-Medical"
]


async def seed():

    # ---------------------------------------
    # 1. Create Tables
    # ---------------------------------------
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables ensured")

    # ---------------------------------------
    # 2. Insert Classes
    # ---------------------------------------
    async with AsyncSessionLocal() as db:
        for name in CLASS_LIST:

            # Check if class already exists
            q = await db.execute(select(models.Class).where(models.Class.name == name))
            if q.scalars().first():
                continue

            # Parse class info
            if "-" in name:
                base, stream = name.split("-")
                base = base.strip()  # "Class 11"
                stream = stream.strip()
                class_number = int(base.split()[1])
                class_in = schemas.ClassCreate(
                    class_number=class_number,
                    stream=stream,
                    name=name
                )
            else:
                class_number = int(name.split()[1])
                class_in = schemas.ClassCreate(
                    class_number=class_number,
                    stream=None,
                    name=name
                )

            # Create entry
            await crud.create_class(db, class_in)

        print("✅ Classes seeded successfully")


if __name__ == "__main__":
    asyncio.run(seed())
