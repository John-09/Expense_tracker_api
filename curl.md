# 1. Create a Category

curl -X POST "http://127.0.0.1:8000/categories" \
 -H "Content-Type: application/json" \
 -d '{
"name": "Food"
}'

---

# 2. Get All Categories

curl "http://127.0.0.1:8000/categories"

---

# 3. Get Category by ID

curl "http://127.0.0.1:8000/categories/1"

---

# 4. Update Category

curl -X PUT "http://127.0.0.1:8000/categories/1" \
 -H "Content-Type: application/json" \
 -d '{
"name": "Food & Drinks"
}'

---

# 5. Create an Expense

curl -X POST "http://127.0.0.1:8000/expenses" \
 -H "Content-Type: application/json" \
 -d '{
"title": "Lunch",
"amount": "250.00",
"description": "Lunch with friends",
"date": "2026-03-10",
"category_id": 1
}'

---

# 6. Get All Expenses

curl "http://127.0.0.1:8000/expenses"

---

# 7. Filter Expenses

## Filter by Category

curl "http://127.0.0.1:8000/expenses?category_id=1"

## Filter by Date Range

curl "http://127.0.0.1:8000/expenses?from_date=2026-03-01&to_date=2026-03-31"

## Filter by Category and Date Range

curl "http://127.0.0.1:8000/expenses?category_id=1&from_date=2026-03-01&to_date=2026-03-31"

---

# 8. Get Expense by ID

curl "http://127.0.0.1:8000/expenses/1"

---

# 9. Update Expense

curl -X PUT "http://127.0.0.1:8000/expenses/1" \
 -H "Content-Type: application/json" \
 -d '{
"title": "Updated Lunch",
"amount": "300.00",
"description": "Updated using cURL",
"date": "2026-03-10",
"category_id": 1
}'

---

# 10. Get Monthly Summary

curl "http://127.0.0.1:8000/summary?month=2026-03"

---

# 11. Delete Expense

curl -X DELETE "http://127.0.0.1:8000/expenses/1"

---

# 12. Verify Expense Deletion

curl -i "http://127.0.0.1:8000/expenses/1"

---

# 13. Delete Category

curl -X DELETE "http://127.0.0.1:8000/categories/1"

---

# 14. Verify Category Deletion

curl -i "http://127.0.0.1:8000/categories/1"
