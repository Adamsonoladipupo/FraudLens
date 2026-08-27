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

  const [selectedTransaction, setSelectedTransaction] =
    useState(null);

  const [investigation, setInvestigation] = useState(null);

  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [investigating, setInvestigating] = useState(false);

  const [error, setError] = useState(null);

  const [riskFilter, setRiskFilter] = useState("");
  const [typeFilter, setTypeFilter] = useState("");

  /*
   * Load dashboard and transaction data.
   */
  useEffect(() => {
    async function loadDashboard() {
      try {
        setError(null);

        if (loading) {
          setLoading(true);
        } else {
          setRefreshing(true);
        }

        const [dashboardData, transactionData] =
          await Promise.all([
            getDashboard(),
            getTransactions({
              riskLevel: riskFilter,
              transactionType: typeFilter,
            }),
          ]);

        setDashboard(dashboardData);
        setTransactions(transactionData);
      } catch (err) {
        console.error("Dashboard loading failed:", err);

        setError(
          err.message ||
            "Unable to load FraudLens dashboard."
        );
      } finally {
        setLoading(false);
        setRefreshing(false);
      }
    }

    loadDashboard();
  }, [riskFilter, typeFilter]);

  /*
   * Refresh dashboard manually.
   */
  async function handleRefresh() {
    try {
      setRefreshing(true);
      setError(null);

      const [dashboardData, transactionData] =
        await Promise.all([
          getDashboard(),
          getTransactions({
            riskLevel: riskFilter,
            transactionType: typeFilter,
          }),
        ]);

      setDashboard(dashboardData);
      setTransactions(transactionData);
    } catch (err) {
      console.error("Refresh failed:", err);

      setError(
        err.message ||
          "Unable to refresh dashboard."
      );
    } finally {
      setRefreshing(false);
    }
  }

  /*
   * Open investigation modal and load investigation data.
   */
  async function handleInvestigate(transactionId) {
    const transaction = transactions.find(
      (item) => item.id === transactionId
    );

    if (!transaction) {
      setError("Transaction could not be found.");
      return;
    }

    /*
     * Open modal immediately using the transaction
     * from the table.
     */
    setSelectedTransaction(transaction);

    /*
     * Clear previous investigation result while the
     * new investigation is loading.
     */
    setInvestigation(null);
    setInvestigating(true);
    setError(null);

    try {
      const result =
        await investigateTransaction(transactionId);

      setInvestigation(result);
    } catch (err) {
      console.error(
        "Investigation failed:",
        err
      );

      setError(
        err.message ||
          "Unable to investigate transaction."
      );
    } finally {
      setInvestigating(false);
    }
  }

  /*
   * Close investigation modal.
   */
  function handleCloseInvestigation() {
    setSelectedTransaction(null);
    setInvestigation(null);
    setInvestigating(false);
  }

  /*
   * Clear transaction filters.
   */
  function clearFilters() {
    setRiskFilter("");
    setTypeFilter("");
  }

  const filtersActive =
    riskFilter !== "" || typeFilter !== "";

  /*
   * Initial loading screen.
   */
  if (loading) {
    return (
      <div className="app">
        <div className="loading-screen">
          <div className="loading-logo">
            FL
          </div>

          <h2>FraudLens</h2>

          <p>
            Loading fraud intelligence dashboard...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      {/* ==================================================
          HEADER
          ================================================== */}
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">
            FL
          </div>

          <div className="brand-copy">
            <strong>FraudLens</strong>

            <span>
              Fraud Intelligence Platform
            </span>
          </div>
        </div>

        <div className="header-right">
          <div className="system-status">
            <span className="status-dot" />

            <span>
              Graph database connected
            </span>
          </div>

          <button
            className="refresh-button"
            onClick={handleRefresh}
            disabled={refreshing}
          >
            <span className="refresh-icon">
              ↻
            </span>

            {refreshing
              ? "Refreshing..."
              : "Refresh"}
          </button>
        </div>
      </header>

      {/* ==================================================
          MAIN DASHBOARD
          ================================================== */}
      <main className="dashboard">
        {/* ==================================================
            HERO
            ================================================== */}
        <section className="hero">
          <div className="hero-content">
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

          <div className="hero-meta">
            <span>LIVE MONITORING</span>

            <span className="hero-indicator" />
          </div>
        </section>

        {/* ==================================================
            ERROR
            ================================================== */}
        {error && (
          <div className="error-banner">
            <div>
              <strong>
                Something went wrong
              </strong>

              <p>{error}</p>
            </div>

            <button
              onClick={() => setError(null)}
              aria-label="Dismiss error"
            >
              ×
            </button>
          </div>
        )}

        {/* ==================================================
            STAT CARDS
            ================================================== */}
        <section className="stats">
          <StatCard
            title="Total Transactions"
            value={
              dashboard?.totalTransactions ?? 0
            }
            description="Total processed"
          />

          <StatCard
            title="Flagged Transactions"
            value={
              dashboard?.flaggedTransactions ?? 0
            }
            description="Require attention"
          />

          <StatCard
            title="High Risk"
            value={
              dashboard?.highRiskTransactions ?? 0
            }
            description="Risk score ≥ 70"
          />

          <StatCard
            title="Fraud Rate"
            value={`${dashboard?.fraudRate ?? 0}%`}
            description="Detected fraud activity"
          />
        </section>

        {/* ==================================================
            TRANSACTION MONITORING
            ================================================== */}
        <section className="transactions-section">
          <div className="section-header">
            <div>
              <span className="eyebrow">
                TRANSACTION MONITORING
              </span>

              <h2>
                Recent transactions
              </h2>

              <p className="section-description">
                Monitor incoming transactions and
                investigate suspicious activity.
              </p>
            </div>

            <div className="section-meta">
              <span className="transaction-count">
                {transactions.length} records
              </span>
            </div>
          </div>

          {/* ==================================================
              FILTERS
              ================================================== */}
          <div className="filters">
            <div className="filter-group">
              <label htmlFor="risk-filter">
                Risk level
              </label>

              <select
                id="risk-filter"
                value={riskFilter}
                onChange={(event) =>
                  setRiskFilter(
                    event.target.value
                  )
                }
              >
                <option value="">
                  All risk levels
                </option>

                <option value="HIGH">
                  High
                </option>

                <option value="MEDIUM">
                  Medium
                </option>

                <option value="LOW">
                  Low
                </option>
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="type-filter">
                Transaction type
              </label>

              <select
                id="type-filter"
                value={typeFilter}
                onChange={(event) =>
                  setTypeFilter(
                    event.target.value
                  )
                }
              >
                <option value="">
                  All transaction types
                </option>

                <option value="PAYMENT">
                  Payment
                </option>

                <option value="PURCHASE">
                  Purchase
                </option>

                <option value="TRANSFER">
                  Transfer
                </option>

                <option value="WITHDRAWAL">
                  Withdrawal
                </option>
              </select>
            </div>

            {filtersActive && (
              <button
                className="clear-filters"
                onClick={clearFilters}
              >
                Clear filters
              </button>
            )}

            {refreshing && (
              <span className="refresh-status">
                Updating transactions...
              </span>
            )}
          </div>

          {/* ==================================================
              TABLE
              ================================================== */}
          <div className="transaction-card">
            <TransactionTable
              transactions={transactions}
              onInvestigate={handleInvestigate}
            />
          </div>
        </section>
      </main>

      {/* ==================================================
          INVESTIGATION MODAL
          ================================================== */}
      {selectedTransaction && (
        <InvestigationPanel
          transaction={selectedTransaction}
          investigation={investigation}
          loading={investigating}
          onClose={handleCloseInvestigation}
        />
      )}
    </div>
  );
}

export default App;