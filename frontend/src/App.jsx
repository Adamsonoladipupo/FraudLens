import { useEffect, useState } from "react";

import StatCard from "./components/StatCard";
import TransactionTable from "./components/TransactionTable";
import InvestigationPanel from "./components/InvestigationPanel";

import {
  getDashboard,
  getTransactions,
  investigateTransaction,
} from "./services/api";

import "./App.css";

function App() {
  const [dashboard, setDashboard] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [investigation, setInvestigation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [dashboardData, transactionData] =
          await Promise.all([
            getDashboard(),
            getTransactions(),
          ]);

        setDashboard(dashboardData);
        setTransactions(transactionData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  async function handleInvestigate(transactionId) {
    try {
      const data = await investigateTransaction(transactionId);
      setInvestigation(data);
    } catch (err) {
      setError(err.message);
    }
  }

  if (loading) {
    return (
      <div className="loading-screen">
        Loading FraudLens...
      </div>
    );
  }

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">FL</div>

          <div>
            <strong>FraudLens</strong>
            <span>Fraud Intelligence Platform</span>
          </div>
        </div>

        <div className="status">
          <span className="status-dot" />
          Graph database connected
        </div>
      </header>

      <main>
        <section className="hero">
          <div>
            <span className="eyebrow">
              FRAUD OPERATIONS
            </span>

            <h1>
              Investigate suspicious
              <br />
              transactions.
            </h1>

            <p>
              Explore connected accounts, devices,
              IP addresses and merchants to uncover
              hidden fraud patterns.
            </p>
          </div>
        </section>

        {error && (
          <div className="error-banner">
            {error}
          </div>
        )}

        <section className="stats">
          <StatCard
            label="Transactions"
            value={dashboard?.transactions ?? 0}
            description="Total processed"
          />

          <StatCard
            label="High Risk"
            value={dashboard?.high_risk_transactions ?? 0}
            description="Require investigation"
          />

          <StatCard
            label="Accounts"
            value={dashboard?.accounts ?? 0}
            description="Bank accounts"
          />

          <StatCard
            label="Devices"
            value={dashboard?.devices ?? 0}
            description="Known devices"
          />
        </section>

        <section className="transactions-section">
          <div className="section-header">
            <div>
              <span className="eyebrow">
                TRANSACTION MONITORING
              </span>

              <h2>Recent transactions</h2>
            </div>

            <span className="transaction-count">
              {transactions.length} records
            </span>
          </div>

          <TransactionTable
            transactions={transactions}
            onInvestigate={handleInvestigate}
          />
        </section>
      </main>

      <InvestigationPanel
        investigation={investigation}
        onClose={() => setInvestigation(null)}
      />
    </div>
  );
}

export default App;
