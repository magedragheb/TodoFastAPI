from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, Item
from schemas import ItemCreate, UserCreate


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    user = await db.execute(select(User).where(User.Id == user_id))
    s = user.scalars()
    return user.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    user = await db.execute(select(User).where(User.Email == email))
    return user.scalars().first()


async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def create_user(db: AsyncSession, user: UserCreate):
    hashed = user.Password + "hash"
    db_user = User(Email=user.Email, Password=hashed)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100):
    items = await db.execute(select(Item).offset(skip).limit(limit))
    return items.scalars().all()


async def create_item(db: AsyncSession, item: ItemCreate, user_id: int):
    db_item = Item(**item.model_dump(), User_Id=user_id)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item
