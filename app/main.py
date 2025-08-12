from contextlib import asynccontextmanager

from fastapi import FastAPI

from .create_db import ensure_database
from .db import init_db
from .routers import transactions


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_database(db_name="ispend_db")
    await init_db()

    yield


app = FastAPI(
    docs_url="/",
    lifespan=lifespan,
)

app.include_router(
    transactions.router,
    prefix="/api/v1/transactions",
    tags=["transactions"],
)
