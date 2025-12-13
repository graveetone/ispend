from contextlib import asynccontextmanager
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.routers import oauth

from .create_db import ensure_database
from .db import init_db
from .routers import transactions, plans, months, categories, health

load_dotenv()


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
        "http://192.168.0.103:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ["SESSION_SECRET_KEY"],
    session_cookie="my_session",
)

routers = [
    dict(router=transactions.router, prefix="/api/v1/transactions", tags=["transactions"]),
    dict(router=plans.router, prefix="/api/v1/plans", tags=["plans"]),
    dict(router=months.router, prefix="/api/v1/months", tags=["months"]),
    dict(router=categories.router, prefix="/api/v1/categories", tags=["categories"]),
    dict(router=oauth.router, prefix="/api/v1/oauth", tags=["oauth"]),
    dict(router=health.router, tags=["health"]),
]

for router_params in routers:
    app.include_router(**router_params)
