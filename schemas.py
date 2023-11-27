from pydantic import BaseModel


class ItemIn(BaseModel):
    Title: str


class ItemOut(BaseModel):
    Id: int
    Title: str
    User_Id: int

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    Id: int
    Email: str
    Is_Active: bool
    Items: list[ItemOut] = []

    class Config:
        from_attributes = True


class UserIn(BaseModel):
    Email: str
    Password: str
    Is_Active: bool = True
