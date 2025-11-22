from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from ..schemas import TransactionType
from ..models import Transaction
from ..db import get_session

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
async def get_categories(
        transaction_type: TransactionType,
        session: AsyncSession = Depends(get_session)
):
    query = select(
        Transaction.category
    ).where(
        Transaction.type == transaction_type
    ).distinct()

    categories = await session.execute(query)
    return categories.scalars().all()
