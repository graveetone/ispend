import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from app.dependencies import get_current_user

from ..schemas import (
    TransactionCreate, TransactionUpdate,
    TransactionType, TransactionModel,
)
from ..models import Transaction
from ..db import get_session

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/", response_model=TransactionModel)
async def create_transaction(
        transaction: TransactionCreate,
        session: AsyncSession = Depends(get_session)
):
    new_transaction = Transaction(**transaction.model_dump())
    session.add(new_transaction)

    await session.commit()
    await session.refresh(new_transaction)

    return new_transaction


@router.get("/", response_model=List[TransactionModel])
async def get_transactions(
        session: AsyncSession = Depends(get_session),
        transaction_type: Optional[TransactionType] = None,
        date: Optional[datetime.date] = None
):
    filters = []

    if transaction_type is not None:
        filters.append(Transaction.type == transaction_type)

    if date is not None:
        filters.append(Transaction.created_at == date)

    query = select(
        Transaction
    ).where(
        *filters
    ).order_by(
        Transaction.amount.desc()
        )

    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{transaction_id}/", response_model=TransactionModel)
async def get_transaction(
        transaction_id: int,
        session: AsyncSession = Depends(get_session)
):
    transaction = await session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.patch("/{transaction_id}/", response_model=TransactionModel)
async def update_transaction(
        transaction_id: int,
        transaction_update: TransactionUpdate,
        session: AsyncSession = Depends(get_session)
):
    transaction = await session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    update_data = transaction_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(transaction, key, value)

    await session.commit()
    await session.refresh(transaction)
    return transaction


@router.delete("/{transaction_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
        transaction_id: int,
        session: AsyncSession = Depends(get_session)
):
    transaction = await session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    await session.delete(transaction)
    await session.commit()
