from sqlalchemy import Column, Integer, String, Float, Date, Enum
from pydantic import BaseModel
from .db import Base
from datetime import date
from typing import Optional
import enum


class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class TransactionModel(BaseModel):
    id: int
    type: TransactionType
    amount: float
    description: str
    category: str
    created_at: date



class Transaction(Base):
    __tablename__ = "transactions"

    id: Optional[int] = Column(Integer, primary_key=True)
    type = Column(Enum(TransactionType))
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    created_at = Column(Date)


class TransactionUpdate(BaseModel):
    type: Optional[TransactionType] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None
    created_at: Optional[date] = None


class TransactionCreate(BaseModel):
    type: TransactionType
    amount: float
    description: str
    category: str
    created_at: date
