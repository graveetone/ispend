from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .create_db import ensure_database
from .db import init_db
from .routers import transactions, plans, months, categories


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_database(force_drop=False)
    await init_db()

    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://i-spend.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = [
    dict(router=transactions.router, prefix="/api/v1/transactions", tags=["transactions"]),
    dict(router=plans.router, prefix="/api/v1/plans", tags=["plans"]),
    dict(router=months.router, prefix="/api/v1/months", tags=["months"]),
    dict(router=categories.router, prefix="/api/v1/categories", tags=["categories"]),
]

for router_params in routers:
    app.include_router(**router_params)
