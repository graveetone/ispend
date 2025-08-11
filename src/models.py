from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional
from enum import Enum


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class TransactionBase(SQLModel):
    type: TransactionType
    amount: float
    description: str
    category: str
    created_at: date


class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class TransactionUpdate(SQLModel):
    type: Optional[TransactionType] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None
    created_at: Optional[date] = None


TransactionCreate = TransactionBase


