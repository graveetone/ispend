import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, func, union

from ..models import Transaction
from ..schemas import MonthCategoryModel, TransactionType
from ..models import Plan
from ..db import get_session

router = APIRouter()


# TODO: add pydantic model for response
@router.get("/{month}")
async def get_month(
        month: datetime.date,
        session: AsyncSession = Depends(get_session)
):
    grouped_transactions_query = (
        select(
            Transaction.category, Transaction.type,
            func.sum(Transaction.amount).label("actual")
        )
        .where(Transaction.created_at == month)
        .group_by(Transaction.category, Transaction.type)
        .subquery()
    )

    plans_query = (
        select(
            Plan,
            Plan.amount.label("planned")
        )
        .where(Plan.month == month)
        .subquery()
    )
    common_select = select(
            func.coalesce(
                plans_query.c.category, grouped_transactions_query.c.category,
            ).label("category"),
            func.coalesce(
                grouped_transactions_query.c.actual, 0,
            ).label("actual"),
            func.coalesce(
                plans_query.c.planned, 0,
            ).label("planned"),
            func.coalesce(
                plans_query.c.type, grouped_transactions_query.c.type,
            ).label("type"),
    )
    left = (
        common_select
        .select_from(
            plans_query.outerjoin(
                grouped_transactions_query,
                plans_query.c.category == grouped_transactions_query.c.category
            )
        )
    )
    right = (
        common_select
        .select_from(
            grouped_transactions_query.outerjoin(
                plans_query,
                plans_query.c.category == grouped_transactions_query.c.category
            )
        )
    )

    joined_transactions_plans_by_category_query = union(left, right)

    results = (await session.execute(joined_transactions_plans_by_category_query)).mappings().all()
    incomes = [
        MonthCategoryModel(**result, month=month)
        for result in results
        if result["type"] == TransactionType.INCOME
    ]
    expenses = [
        MonthCategoryModel(**result, month=month)
        for result in results
        if result["type"] == TransactionType.EXPENSE
    ]
    return {
        "month": month,
        "incomes": incomes,
        "expenses": expenses,
        "total": {
            "incomes": {
                "actual": sum(inc.actual for inc in incomes),
                "planned": sum(inc.planned for inc in incomes),
            },
            "expenses": {
                "actual": sum(exp.actual for exp in expenses),
                "planned": sum(exp.planned for exp in expenses),
            },
        }
    }
