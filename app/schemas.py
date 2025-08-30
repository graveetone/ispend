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

    @classmethod
    def from_orm(cls, obj):
        params = {
            **obj.__dict__,
            "category": obj.category.title if obj.category else None
        }
        return cls(**params)


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
