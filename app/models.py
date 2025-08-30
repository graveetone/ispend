from typing import Optional, List

from sqlalchemy import Column, Integer, String, Float, Date, Enum, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from .db import Base
from .schemas import TransactionType


class Transaction(Base):
    __tablename__ = "transactions"

    id: Optional[int] = Column(Integer, primary_key=True)
    type = Column(Enum(TransactionType))
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(
        "Category", back_populates="transactions", lazy="joined"
    )
    created_at = Column(Date)


class Category(Base):
    __tablename__ = "categories"

    id: Optional[int] = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, index=True, unique=True)

    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction", back_populates="category"
    )
