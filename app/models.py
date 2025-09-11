from typing import Optional

from sqlalchemy import Column, Integer, String, Float, Date, Enum, Index
from .db import Base
from .schemas import TransactionType


class Transaction(Base):
    __tablename__ = "transactions"

    id: Optional[int] = Column(Integer, primary_key=True)
    type = Column(Enum(TransactionType))
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    created_at = Column(Date)


class Plan(Base):
    __tablename__ = "plans"
    __table_args__ = (
        Index('category_month_type', "category", "month", "type", unique=True),
    )

    id: Optional[int] = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    month = Column(Date)
    type = Column(Enum(TransactionType))
