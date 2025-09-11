from contextlib import asynccontextmanager

from fastapi import FastAPI

from .create_db import ensure_database
from .db import init_db
from .routers import transactions, plans, months


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_database(force_drop=False)
    await init_db()

    yield


app = FastAPI(lifespan=lifespan)

routers = [
    dict(router=transactions.router, prefix="/api/v1/transactions", tags=["transactions"]),
    dict(router=plans.router, prefix="/api/v1/plans", tags=["plans"]),
    dict(router=months.router, prefix="/api/v1/months", tags=["months"]),
]

for router_params in routers:
    app.include_router(**router_params)
