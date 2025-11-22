import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from ..schemas import PlanCreate, PlanModel
from ..models import Plan
from ..db import get_session

router = APIRouter()


@router.post("/", response_model=PlanModel)
async def create__or_edit_plan(
        plan_data: PlanCreate,
        session: AsyncSession = Depends(get_session)
):
    plan_data.month = plan_data.month.replace(day=1)

    query = select(Plan).where(
        Plan.category == plan_data.category,
        Plan.month == plan_data.month,
    )

    result = await session.execute(query)
    plan = result.scalar_one_or_none()

    if plan:
        for k, v in plan_data.model_dump().items():
            setattr(plan, k, v)
    else:
        plan = Plan(**plan_data.model_dump())
        session.add(plan)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail=f"Plan for category {plan.category} for {plan.month} already exists",
        )
    await session.refresh(plan)
    return plan


@router.get("/", response_model=PlanModel)
async def get_plan_by_category_and_month(
        category: str, month: datetime.date,
        session: AsyncSession = Depends(get_session)
):
    query = select(Plan).where(
        Plan.category == category,
        Plan.month == month.replace(day=1),
    )

    result = await session.execute(query)
    plan = result.scalars().first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan
