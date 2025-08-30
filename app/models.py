from typing import Optional

from sqlalchemy import Column, Integer, String, Float, Date, Enum
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
