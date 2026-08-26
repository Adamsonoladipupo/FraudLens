import RiskBadge from "./RiskBadge";

function TransactionTable({
  transactions = [],
  onInvestigate,
}) {
  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Transaction</th>
            <th>Amount</th>
            <th>Risk Score</th>
            <th>Risk Level</th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          {transactions.map((transaction) => {
            const riskLevel =
              transaction.riskScore >= 70
                ? "HIGH"
                : transaction.riskScore >= 40
                  ? "MEDIUM"
                  : "LOW";

            return (
              <tr key={transaction.id}>
                <td>
                  <strong>{transaction.id}</strong>
                </td>

                <td>
                  {transaction.currency || "USD"}{" "}
                  {Number(transaction.amount).toLocaleString(
                    undefined,
                    {
                      minimumFractionDigits: 2,
                    }
                  )}
                </td>

                <td>{transaction.riskScore}</td>

                <td>
                  <RiskBadge level={riskLevel} />
                </td>

                <td>
                  <button
                    className="investigate-button"
                    onClick={() => onInvestigate(transaction.id)}
                  >
                    Investigate
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default TransactionTable;
