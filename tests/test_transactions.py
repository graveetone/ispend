import pytest


@pytest.mark.asyncio
async def test_create_transaction(client_factory):
    async with client_factory() as client:
        response = await client.post("/", json={
            "type": "income",
            "amount": 100.5,
            "description": "Test income",
            "category": "Salary",
            "created_at": "2025-08-11"
        })

    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test income"
    assert data["amount"] == 100.5
    assert data["id"] == 3


@pytest.mark.asyncio
async def test_get_all_transactions(client_factory):
    async with client_factory() as client:
        response = await client.get("/")

    assert response.status_code == 200
    transactions = response.json()
    assert len(transactions) == 2


@pytest.mark.asyncio
async def test_get_transaction(client_factory, transactions):
    transaction_id = 2
    async with client_factory() as client:
        response = await client.get(f"/{transaction_id}/")

    assert response.status_code == 200
    transaction = response.json()
    assert transaction == {
        **transactions[transaction_id - 1],
        "id": transaction_id,
    }


@pytest.mark.asyncio
async def test_delete_transaction(client_factory, transactions):
    transaction_id = 2

    async with client_factory() as client:
        delete_response = await client.delete(f"/{transaction_id}/")

    async with client_factory() as client:
        response = await client.get(f"/api/v1/transactions/{transaction_id}/")

    assert delete_response.status_code == 204
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_transaction(client_factory):
    transaction_id = 2

    update_data = {
        "amount": 5442.5,
        "description": "Test income NEW",
        "category": "Salary NEW",
        "created_at": "2025-08-15"
    }
    async with client_factory() as client:
        response = await client.patch(f"/{transaction_id}/", json=update_data)

    assert response.status_code == 200
    data = response.json()

    for k, v in update_data.items():
        assert data[k] == v
