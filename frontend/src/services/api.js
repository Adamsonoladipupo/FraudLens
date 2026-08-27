const API_BASE_URL =
  "https://fraudlens-backend-api.onrender.com";

export async function getTransactions() {
  const response = await fetch(
    `${API_BASE_URL}/api/transactions`
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch transactions: ${response.status}`
    );
  }

  return response.json();
}

export async function getDashboard() {
  const response = await fetch(
    `${API_BASE_URL}/api/dashboard`
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch dashboard: ${response.status}`
    );
  }

  return response.json();
}

export async function investigateTransaction(
  transactionId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/investigations/${transactionId}`
  );

  if (!response.ok) {
    throw new Error(
      `Failed to investigate transaction: ${response.status}`
    );
  }

  return response.json();
}