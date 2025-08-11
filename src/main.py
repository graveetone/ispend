from fastapi import FastAPI
from .db import init_db
from .routers import transactions

app = FastAPI(
    docs_url="/"
)

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["transactions"])
