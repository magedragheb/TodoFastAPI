from datetime import datetime
from database import Base
from sqlalchemy import Boolean, ForeignKey, String, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "Users"
    Id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    Email: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    Password: Mapped[str] = mapped_column(String(50), nullable=False, deferred=True)
    Is_Active: Mapped[bool] = mapped_column(Boolean, default=True)
    # Created_At: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

    Items = relationship("Item", back_populates="User", lazy="select")


class Item(Base):
    __tablename__ = "Items"
    Id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    Title: Mapped[str] = mapped_column(String(50), nullable=False)
    User_Id: Mapped[int] = mapped_column(Integer, ForeignKey("Users.Id"))

    User = relationship("User", back_populates="Items")
