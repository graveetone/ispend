import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import StaticPool
import asyncio
from typing import AsyncGenerator

# Assuming your app structure - adjust imports as needed
from src.routers.transactions import router as transaction_router
from src.models import Transaction, TransactionCreate, TransactionUpdate
from src.db import get_session


# Async database setup
@pytest_asyncio.fixture
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    """Create async test database session"""
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:mysecretpassword@localhost/testdb",
        # connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def async_client(async_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create async test client with dependency override"""

    async def get_session_override():
        yield async_session

    app = FastAPI()
    app.include_router(transaction_router, prefix="/transactions")
    app.dependency_overrides[get_session] = get_session_override

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


class TestAsyncTransactionAPIEndpoints:
    """Async HTTP integration tests for transaction endpoints"""

    @pytest.mark.asyncio
    async def test_create_transaction_success(self, async_client: AsyncClient):
        """Test POST /transactions/ - successful creation"""
        transaction_data = {
            "amount": 100.50,
            "description": "Test transaction",
            "category": "food",
            "type": "income",
            "created_at": "2025-08-03"
        }

        response = await async_client.post("/transactions/", json=transaction_data)

        assert response.status_code == 200
        data = response.json()
        assert data["amount"] == 100.50
        assert data["description"] == "Test transaction"
        assert data["category"] == "food"
        assert "id" in data

    @pytest.mark.asyncio
    async def test_create_transaction_invalid_data(self, async_client: AsyncClient):
        """Test POST /transactions/ - invalid data"""
        # Missing required fields
        invalid_data = {
            "description": "Incomplete transaction"
        }

        response = await async_client.post("/transactions/", json=invalid_data)

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_create_transaction_invalid_json(self, async_client: AsyncClient):
        """Test POST /transactions/ - invalid JSON"""
        response = await async_client.post(
            "/transactions/",
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 422

    # @pytest.mark.asyncio
    # async def test_read_transactions_empty(self, async_client: AsyncClient):
    #     """Test GET /transactions/ - empty database"""
    #     response = await async_client.get("/transactions/")
    #
    #     assert response.status_code == 200
    #     assert response.json() == []

    @pytest.mark.asyncio
    async def test_read_transactions_with_data(self, async_client: AsyncClient):
        """Test GET /transactions/ - with existing data"""
        # Create test transactions
        transactions_data = [
            {
                "amount": 100.50,
                "description": "Transaction 1",
                "category": "food",
                "type": "expense",
                "created_at": "2024-05-02"
            },
            {
                "amount": 200.75,
                "description": "Transaction 2",
                "category": "transport",
                "type": "expense",
                "created_at": "2024-05-02"
            }
        ]

        # Create transactions
        created_ids = []
        for transaction_data in transactions_data:
            response = await async_client.post("/transactions/", json=transaction_data)
            assert response.status_code == 200
            created_ids.append(response.json()["id"])

        # Get all transactions
        response = await async_client.get("/transactions/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2

        # assert data[0]["amount"] == 100.50
        # assert data[1]["amount"] == 200.75

    @pytest.mark.asyncio
    async def test_read_single_transaction_success(self, async_client: AsyncClient):
        """Test GET /transactions/{id} - successful retrieval"""
        # Create a transaction first
        transaction_data = {
            "amount": 150.25,
            "description": "Single transaction test",
            "category": "entertainment",
            "type": "expense",
            "created_at": "2024-05-03"
        }

        create_response = await async_client.post("/transactions/", json=transaction_data)
        assert create_response.status_code == 200
        transaction_id = create_response.json()["id"]

        # Retrieve the transaction
        response = await async_client.get(f"/transactions/{transaction_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == transaction_id
        assert data["amount"] == 150.25
        assert data["description"] == "Single transaction test"

    @pytest.mark.asyncio
    async def test_read_single_transaction_not_found(self, async_client: AsyncClient):
        """Test GET /transactions/{id} - transaction not found"""
        response = await async_client.get("/transactions/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Transaction not found"

    @pytest.mark.asyncio
    async def test_read_single_transaction_invalid_id(self, async_client: AsyncClient):
        """Test GET /transactions/{id} - invalid ID format"""
        response = await async_client.get("/transactions/invalid")

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_update_transaction_success(self, async_client: AsyncClient):
        """Test PATCH /transactions/{id} - successful update"""
        # Create a transaction first
        transaction_data = {
            "amount": 100.00,
            "description": "Original description",
            "category": "food",
            "type": "expense",
            "created_at": "2024-05-03"
        }

        create_response = await async_client.post("/transactions/", json=transaction_data)
        assert create_response.status_code == 200
        transaction_id = create_response.json()["id"]

        # Update the transaction
        update_data = {
            "amount": 150.75,
            "description": "Updated description"
        }

        response = await async_client.patch(f"/transactions/{transaction_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == transaction_id
        assert data["amount"] == 150.75
        assert data["description"] == "Updated description"
        assert data["category"] == "food"  # Should remain unchanged

    @pytest.mark.asyncio
    async def test_update_transaction_partial(self, async_client: AsyncClient):
        """Test PATCH /transactions/{id} - partial update"""
        # Create a transaction first
        transaction_data = {
            "amount": 100.00,
            "description": "Original description",
            "category": "food",
            "type": "expense",
            "created_at": "2024-05-03"
        }

        create_response = await async_client.post("/transactions/", json=transaction_data)
        transaction_id = create_response.json()["id"]

        # Update only amount
        update_data = {"amount": 200.50}

        response = await async_client.patch(f"/transactions/{transaction_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["amount"] == 200.50
        assert data["description"] == "Original description"  # Unchanged

    @pytest.mark.asyncio
    async def test_update_transaction_not_found(self, async_client: AsyncClient):
        """Test PATCH /transactions/{id} - transaction not found"""
        update_data = {"amount": 150.75}

        response = await async_client.patch("/transactions/999", json=update_data)

        assert response.status_code == 404
        assert response.json()["detail"] == "Transaction not found"

    @pytest.mark.asyncio
    async def test_update_transaction_invalid_data(self, async_client: AsyncClient):
        """Test PATCH /transactions/{id} - invalid update data"""
        # Create a transaction first
        transaction_data = {
            "amount": 100.00,
            "description": "Test transaction",
            "category": "food",
            "type": "expense",
            "created_at": "2024-05-03"
        }

        create_response = await async_client.post("/transactions/", json=transaction_data)
        transaction_id = create_response.json()["id"]

        # Try to update with invalid data type
        invalid_update = {"amount": "not_a_number"}

        response = await async_client.patch(f"/transactions/{transaction_id}", json=invalid_update)

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_delete_transaction_success(self, async_client: AsyncClient):
        """Test DELETE /transactions/{id} - successful deletion"""
        # Create a transaction first
        transaction_data = {
            "amount": 100.00,
            "description": "To be deleted",
            "category": "food",
            "type": "expense",
            "created_at": "2024-05-03"
        }

        create_response = await async_client.post("/transactions/", json=transaction_data)
        transaction_id = create_response.json()["id"]

        # Delete the transaction
        response = await async_client.delete(f"/transactions/{transaction_id}")

        assert response.status_code == 204
        assert response.content == b""

        # Verify it's deleted
        get_response = await async_client.get(f"/transactions/{transaction_id}")
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_transaction_not_found(self, async_client: AsyncClient):
        """Test DELETE /transactions/{id} - transaction not found"""
        response = await async_client.delete("/transactions/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Transaction not found"

    @pytest.mark.asyncio
    async def test_delete_transaction_invalid_id(self, async_client: AsyncClient):
        """Test DELETE /transactions/{id} - invalid ID format"""
        response = await async_client.delete("/transactions/invalid")

        assert response.status_code == 422


class TestAsyncTransactionAPIWorkflows:
    """Test complete async workflows and edge cases"""

    @pytest.mark.asyncio
    async def test_full_crud_workflow(self, async_client: AsyncClient):
        """Test complete CRUD workflow via async HTTP"""
        # CREATE
        transaction_data = {
            "amount": 100.00,
            "description": "CRUD test transaction",
            "category": "test",
            "type": "expense",
            "created_at": "2024-05-03"
        }

        create_response = await async_client.post("/transactions/", json=transaction_data)
        assert create_response.status_code == 200
        transaction_id = create_response.json()["id"]

        # READ (single)
        read_response = await async_client.get(f"/transactions/{transaction_id}")
        assert read_response.status_code == 200
        assert read_response.json()["description"] == "CRUD test transaction"

        # UPDATE
        update_data = {"description": "Updated CRUD test"}
        update_response = await async_client.patch(f"/transactions/{transaction_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["description"] == "Updated CRUD test"

        # READ (verify update)
        read_updated_response = await async_client.get(f"/transactions/{transaction_id}")
        assert read_updated_response.status_code == 200
        assert read_updated_response.json()["description"] == "Updated CRUD test"

        # DELETE
        delete_response = await async_client.delete(f"/transactions/{transaction_id}")
        assert delete_response.status_code == 204

        # READ (verify deletion)
        read_deleted_response = await async_client.get(f"/transactions/{transaction_id}")
        assert read_deleted_response.status_code == 404

    @pytest.mark.asyncio
    @pytest.mark.skip
    async def test_concurrent_requests(self, async_client: AsyncClient):
        """Test concurrent async requests"""
        # Create multiple transactions concurrently
        transaction_data_list = [
            {"amount": 100.0 + i, "description": f"Concurrent transaction {i}", "category": "test", "type": "income", "created_at": "2025-08-05"}
            for i in range(5)
        ]

        # Use asyncio.gather for concurrent requests
        create_tasks = [
            async_client.post("/transactions/", json=data)
            for data in transaction_data_list
        ]

        responses = await asyncio.gather(*create_tasks)

        # Verify all requests succeeded
        for response in responses:
            assert response.status_code == 200

        transaction_ids = [response.json()["id"] for response in responses]

        # Read all transactions concurrently
        read_tasks = [
            async_client.get(f"/transactions/{tid}")
            for tid in transaction_ids
        ]

        read_responses = await asyncio.gather(*read_tasks)

        # Verify all reads succeeded
        for i, response in enumerate(read_responses):
            assert response.status_code == 200
            assert response.json()["description"] == f"Concurrent transaction {i}"

    @pytest.mark.asyncio
    async def test_multiple_transactions_workflow(self, async_client: AsyncClient):
        """Test workflow with multiple transactions"""
        transactions_data = [
            {"amount": 50.0, "description": "Transaction 1", "category": "food", "type": "expense", "created_at": "2024-05-03"},
            {"amount": 75.0, "description": "Transaction 2", "category": "transport", "type": "expense", "created_at": "2024-05-03"},
            {"amount": 100.0, "description": "Transaction 3", "category": "entertainment", "type": "expense", "created_at": "2024-05-03"}
        ]

        created_ids = []

        # Create multiple transactions
        for transaction_data in transactions_data:
            response = await async_client.post("/transactions/", json=transaction_data)
            assert response.status_code == 200
            created_ids.append(response.json()["id"])

        # Get all transactions
        all_response = await async_client.get("/transactions/")
        assert all_response.status_code == 200
        assert len(all_response.json()) >= 3

        # Update middle transaction
        update_response = await async_client.patch(
            f"/transactions/{created_ids[1]}",
            json={"amount": 200.0}
        )
        assert update_response.status_code == 200
        assert update_response.json()["amount"] == 200.0

        # Delete first transaction
        delete_response = await async_client.delete(f"/transactions/{created_ids[0]}")
        assert delete_response.status_code == 204

        # Verify remaining transactions
        remaining_response = await async_client.get("/transactions/")
        assert remaining_response.status_code == 200
        remaining_data = remaining_response.json()
        assert len(remaining_data) >= 2

        # Verify the updated transaction is still there with new amount
        updated_transaction = next(
            (t for t in remaining_data if t["id"] == created_ids[1]),
            None
        )
        assert updated_transaction is not None
        assert updated_transaction["amount"] == 200.0

    @pytest.mark.asyncio
    async def test_database_state_consistency(self, async_client: AsyncClient, async_session: AsyncSession):
        """Test database state consistency across async operations"""
        # Create transaction via API
        transaction_data = {
            "amount": 100.0,
            "description": "Consistency test",
            "category": "test",
            "type": "expense",
            "created_at": "2024-05-03"
        }

        create_response = await async_client.post("/transactions/", json=transaction_data)
        assert create_response.status_code == 200
        transaction_id = create_response.json()["id"]

        # Verify via direct database query
        result = await async_session.execute(
            select(Transaction).where(Transaction.id == transaction_id)
        )
        db_transaction = result.scalar_one_or_none()
        assert db_transaction is not None
        assert db_transaction.amount == 100.0
        assert db_transaction.description == "Consistency test"

        # Update via API
        update_response = await async_client.patch(
            f"/transactions/{transaction_id}",
            json={"amount": 150.0}
        )
        assert update_response.status_code == 200

        # Refresh and verify database state
        await async_session.refresh(db_transaction)
        assert db_transaction.amount == 150.0

    @pytest.mark.parametrize("invalid_id", ["abc", "-1", "0", "999999"])
    @pytest.mark.asyncio
    async def test_invalid_transaction_ids(self, async_client: AsyncClient, invalid_id):
        """Test various invalid transaction IDs"""
        # Skip numeric IDs that would pass validation but not exist
        if invalid_id.lstrip('-').isdigit():
            response = await async_client.get(f"/transactions/{invalid_id}")
            assert response.status_code == 404
        else:
            response = await async_client.get(f"/transactions/{invalid_id}")
            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_request_headers_and_content_type(self, async_client: AsyncClient):
        """Test proper handling of headers and content types"""
        transaction_data = {
            "amount": 100.0,
            "description": "Header test",
            "category": "test",
            "type": "expense",
            "created_at": "2024-05-03"
        }

        # Test with explicit JSON content type
        response = await async_client.post(
            "/transactions/",
            json=transaction_data,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200

        # Test response content type
        assert "application/json" in response.headers.get("content-type", "")


# Async performance and load testing
class TestAsyncTransactionAPIPerformance:
    """Async performance tests"""

    @pytest.mark.asyncio
    @pytest.mark.skip
    async def test_concurrent_bulk_operations(self, async_client: AsyncClient):
        """Test performance with concurrent bulk operations"""
        import time

        # Create multiple transactions concurrently
        start_time = time.time()

        create_tasks = []
        for i in range(20):  # Reduced for faster testing
            transaction_data = {
                "amount": float(i * 10),
                "description": f"Bulk transaction {i}",
                "category": "test",
                "type": "expense",
                "created_at": "2024-05-03"
            }
            create_tasks.append(async_client.post("/transactions/", json=transaction_data))

        responses = await asyncio.gather(*create_tasks)
        creation_time = time.time() - start_time

        # Verify all succeeded
        transaction_ids = []
        for response in responses:
            assert response.status_code == 200
            transaction_ids.append(response.json()["id"])

        # Get all transactions
        start_time = time.time()
        response = await async_client.get("/transactions/")
        retrieval_time = time.time() - start_time

        assert response.status_code == 200
        assert len(response.json()) == 20

        # Basic performance assertions (adjust thresholds as needed)
        assert creation_time < 5.0  # Concurrent creates should be faster
        assert retrieval_time < 1.0  # Retrieval should be fast

        print(f"Concurrent creation time for 20 transactions: {creation_time:.2f}s")
        print(f"Retrieval time for 20 transactions: {retrieval_time:.2f}s")

    @pytest.mark.asyncio
    @pytest.mark.skip
    async def test_mixed_concurrent_operations(self, async_client: AsyncClient):
        """Test mixed CRUD operations concurrently"""
        # Create some initial transactions
        initial_data = [
            {"amount": 100.0, "description": f"Initial {i}", "category": "test", "type": "income", "created_at": "2024-06-02"}
            for i in range(5)
        ]

        create_responses = await asyncio.gather(*[
            async_client.post("/transactions/", json=data)
            for data in initial_data
        ])

        transaction_ids = [resp.json()["id"] for resp in create_responses]

        # Perform mixed operations concurrently
        mixed_tasks = []

        # Add some read operations
        mixed_tasks.extend([
            async_client.get(f"/transactions/{tid}")
            for tid in transaction_ids[:2]
        ])

        # Add some update operations
        mixed_tasks.extend([
            async_client.patch(f"/transactions/{tid}", json={"amount": 200.0})
            for tid in transaction_ids[2:4]
        ])

        # Add a delete operation
        mixed_tasks.append(
            async_client.delete(f"/transactions/{transaction_ids[4]}")
        )

        # Add a list operation
        mixed_tasks.append(async_client.get("/transactions/"))

        # Execute all operations concurrently
        responses = await asyncio.gather(*mixed_tasks)

        # Verify responses (adjust indices based on operations above)
        assert responses[0].status_code == 200  # read
        assert responses[1].status_code == 200  # read
        assert responses[2].status_code == 200  # update
        assert responses[3].status_code == 200  # update
        assert responses[4].status_code == 204  # delete
        assert responses[5].status_code == 200  # list


# Event loop fixture for pytest-asyncio
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()