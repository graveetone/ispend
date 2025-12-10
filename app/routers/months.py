import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.sql.functions import coalesce

from ..models import Transaction
from ..schemas import TransactionType
from ..models import Plan
from ..db import get_session

router = APIRouter()


# # TODO: add pydantic model for response
@router.get("/{month}")
async def get_month_new(
        month: datetime.date,
        session: AsyncSession = Depends(get_session)
):
    # month is a datetime.date or string ("2025-02-01")
    month = month.replace(day=1)

    tq = select(
        Transaction.type.label("type"),
        Transaction.category.label("category"),
        func.sum(Transaction.amount).label("actual"),
    ).where(
        func.extract("year", Transaction.created_at) == month.year,
        func.extract("month", Transaction.created_at) == month.month
    ).group_by(
        Transaction.category,
        Transaction.type
    ).subquery()

    pq = select(
        Plan.type.label("type"),
        Plan.amount.label("planned"),
        Plan.category.label("category"),
    ).where(
        Plan.month == month
    ).group_by(
        Plan.type,
        Plan.category,
        Plan.amount,
    ).subquery()

    query = select(
        coalesce(tq.c.type, pq.c.type).label("type"),
        coalesce(tq.c.category, pq.c.category).label("category"),
        tq.c.actual,
        pq.c.planned
    ).select_from(
        tq.join(
            pq,
            (tq.c.category == pq.c.category) &
            (tq.c.type == pq.c.type),
            isouter=True,
            full=True
        )
    ).order_by(
        tq.c.actual.desc(),
        pq.c.planned.desc(),
    )

    result = await session.execute(query)
    result = result.mappings().all()
    incomes = [tx for tx in result if tx.type == TransactionType.INCOME]
    expenses = [tx for tx in result if tx.type == TransactionType.EXPENSE]
    return {
        "month": month,
        "incomes": incomes,
        "expenses": expenses,
        "total": {
            "expenses": {
                "planned": sum((e["planned"] for e in expenses if e["planned"]), start=0.0),
                "actual": sum((e["actual"] for e in expenses if e["actual"]), start=0.0),
            },
            "incomes": {
                "planned": sum((i["planned"] for i in incomes if i["planned"]), start=0.0),
                "actual": sum((i["actual"] for i in incomes if i["actual"]), start=0.0),
            }
        }
    }
