from database import Base
from sqlalchemy import Boolean, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "Users"
    Id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    Email: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    Password: Mapped[str] = mapped_column(String(50), nullable=False, deferred=True)
    Is_Active: Mapped[bool] = mapped_column(Boolean, default=True)

    Items = relationship("Item", back_populates="User", lazy="selectin")


class Item(Base):
    __tablename__ = "Items"
    Id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    Title: Mapped[str] = mapped_column(String(50), nullable=False)
    User_Id: Mapped[int] = mapped_column(Integer, ForeignKey("Users.Id"))

    User = relationship("User", back_populates="Items")
