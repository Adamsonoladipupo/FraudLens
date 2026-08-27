function formatTimestamp(timestamp) {
  if (!timestamp) {
    return "—";
  }

  const date = new Date(timestamp);

  if (Number.isNaN(date.getTime())) {
    return "—";
  }

  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

function getRiskLevel(score) {
  if (score >= 70) {
    return "HIGH";
  }

  if (score >= 40) {
    return "MEDIUM";
  }

  return "LOW";
}

function RiskBadge({ score }) {
  const level = getRiskLevel(score);

  return (
    <span
      className={`risk-badge risk-${level.toLowerCase()}`}
    >
      <span className="risk-dot" />
      {level}
    </span>
  );
}

function TransactionTable({
  transactions,
  onInvestigate,
}) {
  if (!transactions || transactions.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-icon">◎</div>

        <h3>No transactions found</h3>

        <p>
          There are no transactions matching the
          current filters.
        </p>
      </div>
    );
  }

  return (
    <div className="transaction-table-wrapper">
      <table className="transaction-table">
        <thead>
          <tr>
            <th>Transaction</th>
            <th>Amount</th>
            <th>Type</th>
            <th>Risk Score</th>
            <th>Risk Level</th>
            <th>Status</th>
            <th>Timestamp</th>
            <th />
          </tr>
        </thead>

        <tbody>
          {transactions.map((transaction) => (
            <tr key={transaction.id}>
              <td>
                <span className="transaction-id">
                  {transaction.id}
                </span>
              </td>

              <td>
                <span className="transaction-amount">
                  {transaction.currency}{" "}
                  {Number(transaction.amount).toLocaleString(
                    "en-US",
                    {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    }
                  )}
                </span>
              </td>

              <td>
                <span className="transaction-type">
                  {transaction.transactionType}
                </span>
              </td>

              <td>
                <span className="risk-score">
                  {transaction.riskScore}
                </span>
              </td>

              <td>
                <RiskBadge
                  score={transaction.riskScore}
                />
              </td>

              <td>
                <span
                  className={`status-badge status-${String(
                    transaction.status
                  ).toLowerCase()}`}
                >
                  {transaction.status}
                </span>
              </td>

              <td>
                <span className="transaction-time">
                  {formatTimestamp(
                    transaction.timestamp
                  )}
                </span>
              </td>

              <td>
                <button
                  className="investigate-button"
                  onClick={() =>
                    onInvestigate(transaction.id)
                  }
                >
                  Investigate
                  <span>→</span>
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TransactionTable;