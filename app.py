import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

db_url = "sqlite+aiosqlite:///users.db" 
engine = create_async_engine(
        db_url, connect_args={"check_same_thread": False})
session = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "Users"
    Id: Mapped[int] = mapped_column(Integer,primary_key=True)
    Name: Mapped[str] = mapped_column(String(50),nullable=False)

class Item(Base):
    __tablename__ = "Items"
    Id: Mapped[int] = mapped_column(Integer,primary_key=True)
    Name: Mapped[str] = mapped_column(String(50),nullable=False)
    UserId: Mapped[int] = mapped_column(Integer,nullable=False)
    # User = mapped_column(User)

class UserBase(BaseModel):
    Name: str

async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = session()
    try:
        yield db
    finally:
        await db.close()

app = FastAPI()

@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    results = await db.execute(select(User))
    users = results.scalars().all()
    return {"users": users}

@app.post("/users")
async def add_user(user: UserBase, db: AsyncSession = Depends(get_db)):
    model = User(Name=user.Name)
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)