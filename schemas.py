from pydantic import BaseModel


class ItemBase(BaseModel):
    Title: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    Id: int
    Owner_Id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    Email: str


class UserCreate(UserBase):
    Password: str


class User(UserBase):
    Id: int
    Is_Active: bool
    Items: list[Item] = []

    class Config:
        from_attributes = True
