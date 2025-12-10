import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("transaction_type, expected_response", [
    ("expense", ["Food", "Hobby"]),
    ("income", ["Salary", "Present"]),
], ids=[
    'expenses categories',
    'incomes categories',
])
async def test_get_categories(client_factory, transaction_type, expected_response):
    async with client_factory() as client:
        response = await client.get("/categories", params={
            "transaction_type": transaction_type
        })

    assert response.status_code == 200
    assert response.json() == expected_response
