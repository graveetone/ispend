import pytest

no_data_response = dict(
    month="2025-09-10",
    incomes=[],
    expenses=[],
    total=dict(
        incomes=dict(actual=0, planned=0),
        expenses=dict(actual=0, planned=0),
    )
)

two_categories_response = dict(
    month="2025-08-12",
    incomes=[],
    expenses=[
        dict(category="Junk food",  type="expense", planned=0, actual=40.01),
        dict(category="Snacks", type="expense", planned=200.0, actual=59.99),
    ],
    total=dict(
        incomes=dict(actual=0, planned=0),
        expenses=dict(actual=100.0, planned=200.0),
    )
)

expense_and_income_response = dict(
    month="2025-08-05",
    incomes=[dict(category="Salary",  type="income", planned=0, actual=100.5)],
    expenses=[dict(category="Food",  type="expense", planned=0, actual=120)],
    total=dict(
        incomes=dict(actual=100.5, planned=0),
        expenses=dict(actual=120, planned=0),
    )
)

no_transactions_response = dict(
    month="2025-09-01",
    incomes=[],
    expenses=[dict(category="Food", type="expense", planned=100.5, actual=0)],
    total=dict(
        incomes=dict(actual=0, planned=0),
        expenses=dict(actual=0, planned=100.5),
    )
)


@pytest.mark.asyncio
@pytest.mark.parametrize("month, expected_response", [
    ("2025-09-10", no_data_response),
    ("2025-08-12", two_categories_response),
    ("2025-08-05", expense_and_income_response),
    ("2025-09-01", no_transactions_response),
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
