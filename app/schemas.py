from pydantic import BaseModel

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


class PlanCreate(BaseModel):
    amount: float
    category: str
    month: date
    type: TransactionType


class PlanModel(BaseModel):
    id: int
    amount: float
    category: str
    month: date
    type: TransactionType
