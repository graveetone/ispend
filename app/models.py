from typing import Optional, List

from sqlalchemy import Column, Integer, String, Float, Date, Enum, ForeignKey, Index
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


class Plan(Base):
    __tablename__ = "plans"
    __table_args__ = (
        Index('category_month', "category_id", "month", unique=True),
    )

    id: Optional[int] = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(
        "Category", back_populates="plans", lazy="joined"
    )
    month = Column(Date)


class Category(Base):
    __tablename__ = "categories"

    id: Optional[int] = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, index=True, unique=True)

    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction", back_populates="category"
    )
    plans: Mapped[List["Plan"]] = relationship(
        "Plan", back_populates="category"
    )
