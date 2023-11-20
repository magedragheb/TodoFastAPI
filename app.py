from http import HTTPStatus
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
import crud
from database import get_db
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from schemas import UserCreate


app = FastAPI()


@app.get("/users")
async def get_users(
    db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100
):
    users = await crud.get_all_users(db, skip, limit)
    return users


@app.get("/users/{id}")
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_id(db, id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users")
async def add_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    await crud.create_user(db, user)
    return HTTPStatus.CREATED


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
