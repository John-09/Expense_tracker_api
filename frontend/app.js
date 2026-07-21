const expenseForm = document.getElementById("expense-form");

const categorySelect = document.getElementById("category");

const expenseTableBody = document.getElementById("expense-table-body");

const summaryMonthInput = document.getElementById("summary-month");

const summaryTableBody = document.getElementById("summary-table-body");

const summaryTotal = document.getElementById("summary-total");

const formMessage = document.getElementById("form-message");

const summaryMessage = document.getElementById("summary-message");

const submitButton = document.getElementById("submit-button");

const loadSummaryButton = document.getElementById("load-summary-button");

function getCurrentDate() {
  return new Date().toISOString().split("T")[0];
}

function getCurrentMonth() {
  return getCurrentDate().slice(0, 7);
}

function formatAmount(amount) {
  const numericAmount = Number(amount);

  return numericAmount.toLocaleString("en-IN", {
    style: "currency",
    currency: "INR",
    minimumFractionDigits: 2,
  });
}

function showFormMessage(message, type) {
  formMessage.textContent = message;
  formMessage.className = `message ${type}`;
}

function showSummaryMessage(message, type) {
  summaryMessage.textContent = message;
  summaryMessage.className = `message ${type}`;
}

async function loadCategories() {
  const graphqlQuery = `
    query {
      categories {
        id
        name
      }
    }
  `;

  try {
    const response = await fetch("/graphql", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        query: graphqlQuery,
      }),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error("Unable to load categories.");
    }

    if (result.errors) {
      throw new Error(result.errors[0].message);
    }

    const categories = result.data.categories;

    categorySelect.innerHTML = "";

    const placeholder = document.createElement("option");

    placeholder.value = "";
    placeholder.textContent = "Select a category";

    categorySelect.appendChild(placeholder);

    for (const category of categories) {
      const option = document.createElement("option");

      option.value = category.id;
      option.textContent = category.name;

      categorySelect.appendChild(option);
    }
  } catch (error) {
    categorySelect.innerHTML = `
      <option value="">
        Failed to load categories
      </option>
    `;

    showFormMessage(error.message, "error");
  }
}

async function loadExpenses() {
  expenseTableBody.innerHTML = `
    <tr>
      <td colspan="5">
        Loading expenses...
      </td>
    </tr>
  `;

  try {
    const response = await fetch("/expenses");

    const expenses = await response.json();

    if (!response.ok) {
      throw new Error(expenses.detail || "Unable to load expenses.");
    }

    renderExpenses(expenses);
  } catch (error) {
    expenseTableBody.innerHTML = `
      <tr>
        <td colspan="5">
          ${error.message}
        </td>
      </tr>
    `;
  }
}

function renderExpenses(expenses) {
  expenseTableBody.innerHTML = "";

  if (expenses.length === 0) {
    expenseTableBody.innerHTML = `
      <tr>
        <td
          colspan="5"
          class="empty-message"
        >
          No expenses found.
        </td>
      </tr>
    `;

    return;
  }

  for (const expense of expenses) {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${expense.title}</td>

      <td>
        ${formatAmount(expense.amount)}
      </td>

      <td>
        ${expense.category.name}
      </td>

      <td>${expense.date}</td>

      <td>
        ${expense.description || "-"}
      </td>
    `;

    expenseTableBody.appendChild(row);
  }
}

async function addExpense(event) {
  event.preventDefault();

  showFormMessage("", "");

  submitButton.disabled = true;
  submitButton.textContent = "Adding...";

  const formData = new FormData(expenseForm);

  const expenseData = {
    title: formData.get("title"),

    amount: formData.get("amount"),

    description: formData.get("description") || null,

    date: formData.get("date"),

    category_id: Number(formData.get("category")),
  };

  try {
    const response = await fetch("/expenses", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(expenseData),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(getErrorMessage(result));
    }

    showFormMessage("Expense added successfully.", "success");

    expenseForm.reset();

    document.getElementById("date").value = getCurrentDate();

    summaryMonthInput.value = expenseData.date.slice(0, 7);

    await Promise.all([loadExpenses(), loadMonthlySummary()]);
  } catch (error) {
    showFormMessage(error.message, "error");
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Add Expense";
  }
}

function getErrorMessage(result) {
  if (typeof result.detail === "string") {
    return result.detail;
  }

  if (Array.isArray(result.detail) && result.detail.length > 0) {
    return result.detail.map((error) => error.msg).join(", ");
  }

  return "Unable to add expense.";
}

async function loadMonthlySummary() {
  const month = summaryMonthInput.value;

  if (!month) {
    showSummaryMessage("Please select a month.", "error");

    return;
  }

  showSummaryMessage("", "");

  summaryTotal.textContent = "Loading summary...";

  summaryTableBody.innerHTML = `
    <tr>
      <td colspan="3">
        Loading...
      </td>
    </tr>
  `;

  try {
    const response = await fetch(`/summary?month=${encodeURIComponent(month)}`);

    const summary = await response.json();

    if (!response.ok) {
      throw new Error(summary.detail || "Unable to load summary.");
    }

    renderSummary(summary);
  } catch (error) {
    summaryTotal.textContent = "";

    summaryTableBody.innerHTML = `
      <tr>
        <td colspan="3">
          Unable to load summary.
        </td>
      </tr>
    `;

    showSummaryMessage(error.message, "error");
  }
}

function renderSummary(summary) {
  summaryTotal.textContent = `Total spend: ${formatAmount(
    summary.total_spend,
  )}`;

  summaryTableBody.innerHTML = "";

  if (summary.categories.length === 0) {
    summaryTableBody.innerHTML = `
      <tr>
        <td
          colspan="3"
          class="empty-message"
        >
          No expenses found for this month.
        </td>
      </tr>
    `;

    return;
  }

  for (const category of summary.categories) {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>
        ${category.category_name}
      </td>

      <td>
        ${formatAmount(category.total)}
      </td>

      <td>
        ${category.percentage}%
      </td>
    `;

    summaryTableBody.appendChild(row);
  }
}

expenseForm.addEventListener("submit", addExpense);

loadSummaryButton.addEventListener("click", loadMonthlySummary);

async function initializePage() {
  const currentDate = getCurrentDate();

  document.getElementById("date").value = currentDate;

  summaryMonthInput.value = getCurrentMonth();

  await Promise.all([loadCategories(), loadExpenses(), loadMonthlySummary()]);
}

initializePage();
