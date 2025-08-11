import asyncio

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from typing import List

from ..models import Transaction, TransactionCreate, TransactionUpdate
from ..db import get_session

router = APIRouter()

@router.post("/", response_model=Transaction)
async def create_transaction(
    transaction: TransactionCreate,
    session: AsyncSession = Depends(get_session)
):
    transaction = Transaction.model_validate(transaction)
    session.add(transaction)

    await session.commit()
    await session.refresh(transaction)
    return transaction


@router.get("/", response_model=List[Transaction])
async def read_transactions(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Transaction))
    transactions = result.scalars().all()
    return transactions


@router.get("/{transaction_id}", response_model=Transaction)
async def read_transaction(transaction_id: int, session: AsyncSession = Depends(get_session)):
    transaction = await session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.patch("/{transaction_id}", response_model=Transaction)
async def update_transaction(
        transaction_id: int,
        transaction_update: TransactionUpdate,
        session: AsyncSession = Depends(get_session)
):
    transaction = await session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    update_data = transaction_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(transaction, key, value)

    # session.add(transaction)
    await session.commit()
    await session.refresh(transaction)
    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: int, session: AsyncSession = Depends(get_session)):
    transaction = await session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    await session.delete(transaction)
    await session.commit()
    return
