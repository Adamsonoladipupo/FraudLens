const API_BASE_URL =

  import.meta.env.VITE_API_URL || "http://localhost:5173";

async function request(endpoint) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`);

  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || "API request failed");
  }import.meta.env.VITE_API_URL || "http://localhost:5173";

  return response.json();
}

export function getDashboard() {
  return request("/api/dashboard");
}

export function getTransactions({
  riskLevel = "",
  transactionType = "",
  limit = 50,
} = {}) {
  const params = new URLSearchParams();

  if (riskLevel) {
    params.set("risk_level", riskLevel);
  }

  if (transactionType) {
    params.set("transaction_type", transactionType);
  }

  params.set("limit", limit);

  return request(`/api/transactions?${params.toString()}`);
}

export function investigateTransaction(transactionId) {
  return request(`/api/investigations/${transactionId}`);
}

export function getSuspiciousPaths(transactionId) {
  return request(
    `/api/investigations/${transactionId}/paths`
  );
}