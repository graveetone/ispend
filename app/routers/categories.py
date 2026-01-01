from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import func, select, union_all

from app.dependencies import get_current_user

from ..schemas import TransactionType
from ..models import Plan, Transaction
from ..db import get_session

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("", status_code=status.HTTP_200_OK)
async def get_categories(
        transaction_type: TransactionType,
        session: AsyncSession = Depends(get_session)
):
    combined = union_all(
        select(
            Transaction.category.label("category")
        ).where(
            Transaction.type == transaction_type
        ),
        select(
            Plan.category.label("category")
        ).where(
            Plan.type == transaction_type
        ),
    ).subquery()

    query = (
        select(
            combined.c.category,
            func.count().label("usage_count")
        )
        .group_by(combined.c.category)
        .order_by(func.count().desc())
    )

    result = await session.execute(query)
    return [row.category for row in result.all()]
