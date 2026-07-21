from decimal import Decimal


def create_category(
    client,
    name: str = "Food",
) -> dict:
    response = client.post(
        "/categories",
        json={
            "name": name,
        },
    )

    assert response.status_code == 201

    return response.json()


def create_expense(
    client,
    category_id: int,
    *,
    title: str = "Lunch",
    amount: str = "250.00",
    expense_date: str = "2026-03-10",
) -> dict:
    response = client.post(
        "/expenses",
        json={
            "title": title,
            "amount": amount,
            "description": "Test expense",
            "date": expense_date,
            "category_id": category_id,
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_and_read_expense(client):
    category = create_category(client)

    created = create_expense(
        client,
        category["id"],
    )

    response = client.get(
        f'/expenses/{created["id"]}'
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Lunch"
    assert Decimal(str(data["amount"])) == Decimal("250.00")
    assert data["category"]["name"] == "Food"


def test_filter_expenses(client):
    food = create_category(
        client,
        "Food",
    )

    travel = create_category(
        client,
        "Travel",
    )

    create_expense(
        client,
        food["id"],
        title="Breakfast",
        amount="100.00",
        expense_date="2026-03-05",
    )

    create_expense(
        client,
        food["id"],
        title="Dinner",
        amount="300.00",
        expense_date="2026-04-05",
    )

    create_expense(
        client,
        travel["id"],
        title="Bus",
        amount="50.00",
        expense_date="2026-03-06",
    )

    response = client.get(
        "/expenses",
        params={
            "category_id": food["id"],
            "from_date": "2026-03-01",
            "to_date": "2026-03-31",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Breakfast"

def test_negative_amount_returns_422(client):
    category = create_category(client)

    response = client.post(
        "/expenses",
        json={
            "title": "Invalid expense",
            "amount": "-10.00",
            "description": None,
            "date": "2026-03-10",
            "category_id": category["id"],
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"]


def test_missing_expense_returns_404(client):
    response = client.get(
        "/expenses/999999"
    )

    assert response.status_code == 404

def test_duplicate_category_returns_409(client):
    create_category(
        client,
        "Food",
    )

    response = client.post(
        "/categories",
        json={
            "name": "Food",
        },
    )

    assert response.status_code == 409


def test_monthly_summary_calculation(client):
    food = create_category(
        client,
        "Food",
    )

    travel = create_category(
        client,
        "Travel",
    )

    create_expense(
        client,
        food["id"],
        title="Groceries",
        amount="100.00",
        expense_date="2026-03-05",
    )

    create_expense(
        client,
        travel["id"],
        title="Taxi",
        amount="200.00",
        expense_date="2026-03-06",
    )

    create_expense(
        client,
        food["id"],
        title="April food",
        amount="500.00",
        expense_date="2026-04-01",
    )

    response = client.get(
        "/summary",
        params={
            "month": "2026-03",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["month"] == "2026-03"

    assert Decimal(
        str(data["total_spend"])
    ) == Decimal("300.00")

    totals = {
        item["category_name"]: Decimal(
            str(item["total"])
        )
        for item in data["categories"]
    }

    assert totals == {
        "Food": Decimal("100.00"),
        "Travel": Decimal("200.00"),
    }