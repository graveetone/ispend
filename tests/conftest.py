import asyncio

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.dependencies import get_current_user
from app.main import app
from app.db import get_session, Base
from app.routers import oauth


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture()
def test_env(monkeypatch):
    monkeypatch.setattr(oauth, "APP_JWT_SECRET", "test-secret")
    monkeypatch.setattr(oauth, "GOOGLE_CLIENT_ID", "test")
    monkeypatch.setattr(oauth, "GOOGLE_CLIENT_SECRET", "test")

    return {
        "APP_JWT_SECRET": "test-secret",
        "GOOGLE_CLIENT_ID": "test",
        "GOOGLE_CLIENT_SECRET": "test",
    }


async def override_get_session() -> AsyncSession:
    async with TestingSessionLocal() as session:
        yield session


def fake_user():
    return "test@test.com"


app.dependency_overrides[get_session] = override_get_session
app.dependency_overrides[get_current_user] = fake_user


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
            "type": "income",
            "amount": 500,
            "description": "present from Sviatyi Mykolai",
            "category": "Present",
            "created_at": "2025-08-04"
        },
        {
            "type": "expense",
            "amount": 59.99,
            "description": "Chips",
            "category": "Food",
            "created_at": "2025-08-12"
        },
        {
            "type": "expense",
            "amount": 40.01,
            "description": "Pepsi",
            "category": "Food",
            "created_at": "2025-10-12"
        },
        {
            "type": "expense",
            "amount": 120,
            "description": "Burger",
            "category": "Food",
            "created_at": "2025-08-05"
        },
        {
            "type": "expense",
            "amount": 400,
            "description": "thrown for the wind",
            "category": "Hobby",
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
            "category": "Food",
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
