import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from ..schemas import (
    TransactionCreate, TransactionUpdate,
    TransactionType, TransactionModel,
)
from ..models import Transaction, Category
from ..db import get_session

router = APIRouter()


@router.post("/", response_model=TransactionModel)
async def create_transaction(
        transaction: TransactionCreate,
        session: AsyncSession = Depends(get_session)
):
    query = select(Category).where(Category.title == transaction.category)
    category = await session.execute(query)
    category = category.scalars().first()

    if category is None:
        category = Category(title=transaction.category)
        session.add(category)
        await session.commit()

    params = transaction.model_dump()
    params.pop("category")
    new_transaction = Transaction(**params)
    new_transaction.category_id = category.id


    session.add(new_transaction)
    await session.commit()
    await session.refresh(new_transaction)
    await session.refresh(category)

    return TransactionModel.from_orm(new_transaction)


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

    query = select(Transaction).where(*filters)

    result = await session.execute(query)
    return [
        TransactionModel.from_orm(transaction)
        for transaction in result.scalars().all()
    ]


@router.get("/{transaction_id}/", response_model=TransactionModel)
async def get_transaction(
        transaction_id: int,
        session: AsyncSession = Depends(get_session)
):
    transaction = await session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return TransactionModel.from_orm(transaction)


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
    category_title = update_data.pop("category")

    for key, value in update_data.items():
        setattr(transaction, key, value)

    query = select(Category).where(Category.title == category_title)
    category = await session.execute(query)
    category = category.scalars().first()

    if category is None:
        category = Category(title=category_title)
        session.add(category)
        await session.commit()

    transaction.category_id = category.id

    await session.commit()
    await session.refresh(transaction)
    return TransactionModel.from_orm(transaction)


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
