import asyncio

import pytest
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from app.create_db import ensure_database, drop_database

from app.main import app
from app.db import get_session


TEST_DATABASE_URL = "postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/ispend_db_test"  # noqa: E501
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


def pytest_collection_modifyitems(config, items):
    if items:
        config.stash['first_test_id'] = items[0].nodeid
        config.stash['last_test_id'] = items[-1].nodeid


@pytest.fixture(autouse=True)
async def prepare_database(request):
    first_test = request.node.nodeid == request.config.stash['first_test_id']
    last_test = request.node.nodeid == request.config.stash['last_test_id']
    if first_test:
        await ensure_database(db_name="ispend_db_test", force_drop=True)
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine_test.dispose()

    if last_test:
        await drop_database()


@pytest.fixture
def client_factory():
    def _wrapper():
        return AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test/api/v1/transactions/",
        )
    return _wrapper


@pytest.fixture
async def client(client_factory):
    async with client_factory() as c:
        yield c


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
        }
    ]


@pytest.fixture(scope="function", autouse=True)
async def seed_database(client_factory, transactions):
    print("Seeding test database")

    async def create_transaction(transaction):
        async with client_factory() as client:
            return await client.post("/", json=transaction)

    async def drop_transaction(transaction_id):
        async with client_factory() as client:
            return await client.delete(f"/{transaction_id}")

    await asyncio.gather(
        *[
            create_transaction(transaction)
            for transaction in transactions
        ]
    )
    yield
    async with client_factory() as client:
        transactions = await client.get("/")

    print("Cleanup test database")
    await asyncio.gather(
        *[
            drop_transaction(transaction["id"])
            for transaction in transactions.json()
        ]
    )
