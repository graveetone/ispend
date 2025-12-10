import pytest

plan_no_transactions_response = dict(
    month="2025-09-01",
    incomes=[],
    expenses=[
        dict(planned=100.5, category="Food", actual=None, type="expense")
    ],
    total=dict(
        incomes=dict(actual=0.0, planned=0.0),
        expenses=dict(actual=0.0, planned=100.5),
    )
)

plan_and_transactions = dict(
    month="2025-08-01",
    incomes=[
        dict(category="Present", actual=500.0, planned=None, type="income"),
        dict(category="Salary", actual=100.5, planned=None, type="income"),
    ],
    expenses=[
        dict(category="Hobby", type="expense", planned=None, actual=400.0),
        dict(category="Food", type="expense", planned=200.0, actual=179.99),
    ],
    total=dict(
        incomes=dict(actual=600.5, planned=0.0),
        expenses=dict(actual=579.99, planned=200.0),
    )
)

transactions_no_plan_response = dict(
    month="2025-10-01",
    incomes=[],
    expenses=[
        dict(category="Food", type="expense", planned=None, actual=40.01)
    ],
    total=dict(
        incomes=dict(actual=0.0, planned=0.0),
        expenses=dict(actual=40.01, planned=0.0),
    )
)


@pytest.mark.asyncio
@pytest.mark.parametrize("month, expected_response", [
    ("2025-09-10", plan_no_transactions_response),
    ("2025-08-12", plan_and_transactions),
    ("2025-10-05", transactions_no_plan_response),
], ids=[
    'plan_no_transactions',
    'plan_and_transactions',
    'transactions_no_plan'
])
async def test_get_month(month, expected_response, client_factory):
    async with client_factory() as client:
        response = await client.get(f"/months/{month}")

    assert response.status_code == 200
    data = response.json()

    assert data['month'] == expected_response['month']
    assert data['total'] == expected_response['total']
    assert data['expenses'] == expected_response['expenses']
    assert data['incomes'] == expected_response['incomes']
