from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
    AsyncAttrs,
)

db_url = "sqlite+aiosqlite:///users.db"
engine: AsyncEngine = create_async_engine(
    db_url, connect_args={"check_same_thread": False}
)
session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db: AsyncSession = session()
    try:
        yield db
    finally:
        await db.close()
