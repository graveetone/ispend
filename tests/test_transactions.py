import pytest


@pytest.mark.asyncio
async def test_create_transaction(client_factory):
    async with client_factory() as client:
        response = await client.post("/transactions/", json={
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
    assert data["id"] == 7


@pytest.mark.parametrize(
    argnames="params,expected_count",
    argvalues=[
        (dict(transaction_type="income", date="2025-08-05"), 1),
        (dict(transaction_type="expense", date="2025-08-12"), 1),
        (dict(transaction_type="expense"), 4),
        (dict(date="2025-08-05"), 3),
        (dict(transaction_type="income", date="2025-08-11"), 0),
    ],
    ids=[
        "Income for specific date",
        "Expense for specific date",
        "All expenses",
        "All transactions for date",
        "No transactions for date"
    ]
)
@pytest.mark.asyncio
async def test_get_all_filtered_transactions(
        client_factory, params, expected_count
):
    async with client_factory() as client:
        response = await client.get("/transactions/", params=params)

    assert response.status_code == 200
    transactions = response.json()
    assert len(transactions) == expected_count


@pytest.mark.asyncio
async def test_get_all_transactions(client_factory, transactions):
    async with client_factory() as client:
        response = await client.get("/transactions/")

    assert response.status_code == 200
    all_transactions = response.json()
    assert len(all_transactions) == len(transactions)


@pytest.mark.asyncio
async def test_get_transaction(client_factory, transactions):
    transaction_id = 2
    async with client_factory() as client:
        response = await client.get(f"/transactions/{transaction_id}/")

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
        delete_response = await client.delete(f"/transactions/{transaction_id}/")

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
        response = await client.patch(f"/transactions/{transaction_id}/", json=update_data)

    assert response.status_code == 200
    data = response.json()

    for k, v in update_data.items():
        assert data[k] == v
