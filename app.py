import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
import crud
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import ItemIn, ItemOut, UserIn, UserOut


app = FastAPI()


@app.get("/users", status_code=status.HTTP_200_OK, response_model=list[UserOut])
async def get_users(
    db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100
):
    return await crud.get_all_users(db, skip, limit)


@app.get("/users/{id}", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_id(db, id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def add_user(user: UserIn, db: AsyncSession = Depends(get_db)) -> UserOut:
    return await crud.create_user(db, user)


@app.post("/items", status_code=status.HTTP_201_CREATED, response_model=ItemOut)
async def add_item(
    id: int, item: ItemIn, db: AsyncSession = Depends(get_db)
) -> ItemOut:
    return await crud.create_item(db, item, id)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
