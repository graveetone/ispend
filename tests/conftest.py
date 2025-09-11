import asyncio

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import get_session, Base


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_session() -> AsyncSession:
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(autouse=True)
async def prepare_database(request):
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine_test.dispose()


@pytest.fixture
def client_factory():
    def _wrapper():
        return AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test/api/v1",
        )
    return _wrapper


@pytest.fixture(scope="session")
def transactions():
    return [
        {
            "type": "income",
            "amount": 100.5,
            "description": "Salary for July",
            "category": "Salary",
            "created_at": "2025-08-05"
        },
        {
            "type": "expense",
            "amount": 59.99,
            "description": "Chips",
            "category": "Snacks",
            "created_at": "2025-08-12"
        },
        {
            "type": "expense",
            "amount": 40.01,
            "description": "Pepsi",
            "category": "Junk food",
            "created_at": "2025-08-12"
        },
        {
            "type": "expense",
            "amount": 120,
            "description": "Burger",
            "category": "Food",
            "created_at": "2025-08-05"
        },
    ]


@pytest.fixture(scope="session")
def plans():
    return [
        {
            "amount": 100.5,
            "category": "Food",
            "month": "2025-09-01",
            "type": "expense",
        },
        {
            "amount": 200,
            "category": "Snacks",
            "month": "2025-08-12",
            "type": "expense",
        }
    ]


@pytest.fixture(scope="function", autouse=True)
async def seed_database(client_factory, transactions, plans):
    print("\nSeeding test database\n")

    async def create_transaction(transaction):
        async with client_factory() as client:
            return await client.post("/transactions/", json=transaction)

    async def create_plan(plan):
        async with client_factory() as client:
            return await client.post("/plans/", json=plan)

    await asyncio.gather(
        *[
            create_transaction(transaction)
            for transaction in transactions
        ],
        *[
            create_plan(plan)
            for plan in plans
        ],
    )

    yield
