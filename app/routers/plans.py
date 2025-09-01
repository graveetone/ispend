import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from ..models import Category
from ..schemas import PlanCreate, PlanModel
from ..models import Plan
from ..db import get_session

router = APIRouter()


@router.post("/", response_model=PlanModel)
async def create_plan(
        plan: PlanCreate,
        session: AsyncSession = Depends(get_session)
):
    query = select(Category).where(Category.title == plan.category)
    category = await session.execute(query)
    category = category.scalars().first()

    if category is None:
        category = Category(title=plan.category)
        session.add(category)
        await session.commit()

    params = plan.model_dump()
    params.pop("category")
    new_plan = Plan(**params)
    new_plan.category_id = category.id

    session.add(new_plan)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail=f"Plan for category {plan.category} for {plan.month} already exists",
        )
    await session.refresh(new_plan)
    await session.refresh(category)

    return PlanModel.from_orm(new_plan)


@router.get("/", response_model=PlanModel)
async def get_plan_by_category_and_month(
        category: str, month: datetime.date,
        session: AsyncSession = Depends(get_session)
):
    query = select(Plan).join(Plan.category).where(
        Category.title == category,
        Plan.month == month,
    ).options(joinedload(Plan.category))

    result = await session.execute(query)
    plan = result.scalars().first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return PlanModel.from_orm(plan)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan(
        category: str, month: datetime.date,
        session: AsyncSession = Depends(get_session)
):
    query = select(Plan).join(Plan.category).where(
        Category.title == category,
        Plan.month == month,
    ).options(joinedload(Plan.category))

    result = await session.execute(query)
    plan = result.scalars().first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    await session.delete(plan)
    await session.commit()
