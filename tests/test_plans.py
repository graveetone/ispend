import pytest


@pytest.mark.asyncio
async def test_create_plan(client_factory):
    params = {
        "amount": 100.5,
        "category": "Salary",
        "month": "2025-08-11",
        "type": "income"
    }
    async with client_factory() as client:
        response = await client.post("/plans/", json=params)

    assert response.status_code == 200
    data = response.json()
    assert {
        **params,
        "id": 3,
        "month": "2025-08-01",  # date should have day as 01
    } == data


@pytest.mark.asyncio
async def test_create_plan_duplicate(client_factory):
    params = {
        "amount": 100.5,
        "category": "Food",
        "month": "2025-09-01",
        "type": "expense"
    }
    async with client_factory() as client:
        response = await client.post("/plans/", json=params)
        assert response.status_code == 200

        response = await client.get("/plans/", params={
            "month": "2025-09-01",
            "category": "Food",
            "type": "expense"
        })

        assert response.status_code == 200
        plan = response.json()

        assert plan["month"] == "2025-09-01"
        assert plan["category"] == "Food"
        assert plan["type"] == "expense"


@pytest.mark.asyncio
async def test_get_plan(client_factory):
    async with client_factory() as client:
        response = await client.get("/plans/", params={
            "month": "2025-09-01",
            "category": "Food",
            "type": "expense"
        })

    assert response.status_code == 200
    plan = response.json()

    assert plan["month"] == "2025-09-01"
    assert plan["category"] == "Food"
    assert plan["type"] == "expense"
