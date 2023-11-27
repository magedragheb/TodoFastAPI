from typing import Sequence, Tuple
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from automapper import mapper
from models import User, Item
from schemas import ItemIn, ItemOut, UserIn, UserOut


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    user: Result[Tuple[User]] = await db.execute(select(User).where(User.Id == user_id))
    return user.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    user: Result[Tuple[User]] = await db.execute(
        select(User).where(User.Email == email)
    )
    return user.scalars().first()


async def get_all_users(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> Sequence[User]:
    result: Result[Tuple[User]] = await db.execute(
        select(User).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_user(db: AsyncSession, user_in: UserIn) -> UserOut:
    user_in.Password = user_in.Password + "hash"
    user = User(**user_in.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    usermap: UserOut = mapper.to(UserOut).map(user)
    return usermap


async def get_items(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> Sequence[Item]:
    items: Result[Tuple[Item]] = await db.execute(
        select(Item).offset(skip).limit(limit)
    )
    return items.scalars().all()


async def create_item(db: AsyncSession, item_in: ItemIn, user_id: int) -> ItemOut:
    item = Item(Title=item_in.Title, User_Id=user_id)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    itemmap: ItemOut = mapper.to(ItemOut).map(item)
    return itemmap
