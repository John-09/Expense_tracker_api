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

def test_graphql_expenses_query(client):
    category = create_category(client)

    create_response = client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": "250.00",
            "description": "GraphQL query test",
            "date": "2026-03-10",
            "category_id": category["id"],
        },
    )

    assert create_response.status_code == 201

    query = """
    query {
      expenses {
        id
        title
        amount
        category {
          id
          name
        }
      }
    }
    """

    response = client.post(
        "/graphql",
        json={
            "query": query,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "data" in body
    assert "errors" not in body

    expense = body["data"]["expenses"][0]

    assert expense["title"] == "Lunch"
    assert expense["category"]["name"] == "Food"


def test_graphql_add_expense_mutation(client):
    category = create_category(client)

    mutation = """
    mutation AddExpense($input: AddExpenseInput!) {
      addExpense(input: $input) {
        id
        title
        amount
        category {
          id
          name
        }
      }
    }
    """

    variables = {
        "input": {
            "title": "Dinner",
            "amount": "420.00",
            "description": "GraphQL mutation test",
            "date": "2026-03-12",
            "categoryId": category["id"],
        }
    }

    response = client.post(
        "/graphql",
        json={
            "query": mutation,
            "variables": variables,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "data" in body
    assert "errors" not in body

    created = body["data"]["addExpense"]

    assert created["title"] == "Dinner"
    assert created["category"]["name"] == "Food"