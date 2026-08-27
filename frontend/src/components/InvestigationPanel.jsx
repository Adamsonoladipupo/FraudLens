import { useEffect } from "react";

import RiskBadge from "./RiskBadge";

function InvestigationPanel({
  transaction,
  investigation,
  loading,
  onClose,
}) {
  /*
   * Allow Escape key to close the modal.
   */
  useEffect(() => {
    function handleKeyDown(event) {
      if (event.key === "Escape") {
        onClose();
      }
    }

    document.addEventListener(
      "keydown",
      handleKeyDown
    );

    return () => {
      document.removeEventListener(
        "keydown",
        handleKeyDown
      );
    };
  }, [onClose]);

  /*
   * Prevent background page scrolling while modal
   * is open.
   */
  useEffect(() => {
    document.body.style.overflow = "hidden";

    return () => {
      document.body.style.overflow = "";
    };
  }, []);

  /*
   * Use investigation data when available.
   * Fall back to the transaction from the table
   * while the investigation request is loading.
   */
  const transactionData =
    investigation?.transaction || transaction;

  const account = investigation?.account;
  const customer = investigation?.customer;
  const merchant = investigation?.merchant;

  const devices =
    investigation?.devices || [];

  const ipAddresses =
    investigation?.ip_addresses || [];

  const connectedAccounts =
    investigation?.connected_accounts || [];

  const connectedIpAccounts =
    investigation?.connected_ip_accounts || [];

  const riskAssessment =
    investigation?.risk_assessment;

  const riskScore =
    riskAssessment?.score ??
    transaction?.riskScore ??
    0;

  const riskLevel =
    riskAssessment?.level ||
    getRiskLevel(riskScore);

  function handleOverlayClick(event) {
    /*
     * Only close when the backdrop itself is clicked.
     */
    if (
      event.target === event.currentTarget
    ) {
      onClose();
    }
  }

  return (
    <div
      className="investigation-overlay"
      onMouseDown={handleOverlayClick}
    >
      <div
        className="investigation-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="investigation-title"
      >
        {/* ==================================================
            MODAL HEADER
            ================================================== */}
        <div className="modal-header">
          <div className="modal-heading">
            <div className="modal-icon">
              FL
            </div>

            <div>
              <span className="eyebrow">
                FRAUD INVESTIGATION
              </span>

              <h2 id="investigation-title">
                {transactionData?.id ||
                  "Transaction Investigation"}
              </h2>

              <p>
                Transaction intelligence and
                connected entity analysis
              </p>
            </div>
          </div>

          <button
            className="close-button"
            onClick={onClose}
            aria-label="Close investigation"
          >
            ×
          </button>
        </div>

        {/* ==================================================
            LOADING STATE
            ================================================== */}
        {loading && (
          <div className="investigation-loading">
            <div className="loading-spinner" />

            <div>
              <strong>
                Analyzing transaction
              </strong>

              <p>
                Searching connected accounts,
                devices, IP addresses and
                merchants...
              </p>
            </div>
          </div>
        )}

        {/* ==================================================
            INVESTIGATION CONTENT
            ================================================== */}
        {!loading && (
          <>
            {/* ==================================================
                RISK SUMMARY
                ================================================== */}
            <div
              className={`risk-summary risk-summary-${riskLevel.toLowerCase()}`}
            >
              <div className="risk-summary-left">
                <span className="summary-label">
                  RISK ASSESSMENT
                </span>

                <div className="risk-score-large">
                  {riskScore}
                  <span>/100</span>
                </div>

                <p>
                  Based on connected entity
                  relationships and detected
                  risk indicators.
                </p>
              </div>

              <div className="risk-summary-right">
                <span className="summary-label">
                  RISK LEVEL
                </span>

                <RiskBadge
                  level={riskLevel}
                />
              </div>
            </div>

            {/* ==================================================
                TRANSACTION DETAILS
                ================================================== */}
            <section className="investigation-section">
              <div className="section-title">
                <div>
                  <span className="section-number">
                    01
                  </span>

                  <div>
                    <h3>
                      Transaction details
                    </h3>

                    <p>
                      Core information about this
                      transaction.
                    </p>
                  </div>
                </div>
              </div>

              <div className="detail-grid">
                <DetailItem
                  label="Transaction ID"
                  value={
                    transactionData?.id
                  }
                  mono
                />

                <DetailItem
                  label="Amount"
                  value={`${transactionData?.currency || "USD"} ${Number(
                    transactionData?.amount || 0
                  ).toLocaleString("en-US", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}`}
                  emphasis
                />

                <DetailItem
                  label="Transaction Type"
                  value={
                    transactionData
                      ?.transactionType
                  }
                />

                <DetailItem
                  label="Status"
                  value={
                    transactionData?.status
                  }
                />

                <DetailItem
                  label="Account"
                  value={
                    account?.id ||
                    transactionData?.accountId ||
                    "N/A"
                  }
                  mono
                />

                <DetailItem
                  label="Customer"
                  value={
                    customer?.id ||
                    "N/A"
                  }
                  mono
                />

                <DetailItem
                  label="Merchant"
                  value={
                    merchant?.name ||
                    merchant?.id ||
                    "N/A"
                  }
                />

                <DetailItem
                  label="Timestamp"
                  value={formatTimestamp(
                    transactionData?.timestamp
                  )}
                />
              </div>
            </section>

            {/* ==================================================
                CONNECTED ENTITIES
                ================================================== */}
            <section className="investigation-section">
              <div className="section-title">
                <div>
                  <span className="section-number">
                    02
                  </span>

                  <div>
                    <h3>
                      Connected entities
                    </h3>

                    <p>
                      Relationships discovered
                      around this transaction.
                    </p>
                  </div>
                </div>
              </div>

              <div className="entity-grid">
                <EntityCard
                  icon="D"
                  title="Devices"
                  items={devices}
                  connectedItems={
                    connectedAccounts
                  }
                  connectedLabel="Shared with"
                />

                <EntityCard
                  icon="IP"
                  title="IP addresses"
                  items={ipAddresses}
                  connectedItems={
                    connectedIpAccounts
                  }
                  connectedLabel="Shared with"
                />
              </div>
            </section>

            {/* ==================================================
                RISK INDICATORS
                ================================================== */}
            <section className="investigation-section">
              <div className="section-title">
                <div>
                  <span className="section-number">
                    03
                  </span>

                  <div>
                    <h3>
                      Risk indicators
                    </h3>

                    <p>
                      Signals contributing to the
                      risk assessment.
                    </p>
                  </div>
                </div>
              </div>

              {riskAssessment?.indicators
                ?.length > 0 ? (
                <div className="indicator-list">
                  {riskAssessment.indicators.map(
                    (indicator, index) => (
                      <div
                        className="indicator"
                        key={
                          indicator.code ||
                          index
                        }
                      >
                        <div className="indicator-icon">
                          !
                        </div>

                        <div>
                          <strong>
                            {indicator.code.replaceAll(
                              "_",
                              " "
                            )}
                          </strong>

                          <span>
                            {
                              indicator.description
                            }
                          </span>
                        </div>
                      </div>
                    )
                  )}
                </div>
              ) : (
                <div className="no-indicators">
                  <span>✓</span>

                  <div>
                    <strong>
                      No suspicious indicators
                    </strong>

                    <p>
                      No significant risk signals
                      were identified for this
                      transaction.
                    </p>
                  </div>
                </div>
              )}
            </section>

            {/* ==================================================
                INVESTIGATION FOOTER
                ================================================== */}
            <div className="modal-footer">
              <div>
                <span className="footer-dot" />

                <span>
                  Investigation complete
                </span>
              </div>

              <button
                className="secondary-button"
                onClick={onClose}
              >
                Close investigation
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

/*
 * Small reusable detail component.
 */
function DetailItem({
  label,
  value,
  mono = false,
  emphasis = false,
}) {
  return (
    <div className="detail-item">
      <span>{label}</span>

      <strong
        className={`${mono ? "mono" : ""} ${
          emphasis ? "detail-emphasis" : ""
        }`}
      >
        {value || "N/A"}
      </strong>
    </div>
  );
}

/*
 * Connected entity card.
 */
function EntityCard({
  icon,
  title,
  items,
  connectedItems,
  connectedLabel,
}) {
  return (
    <div className="entity-card">
      <div className="entity-card-header">
        <div className="entity-icon">
          {icon}
        </div>

        <div>
          <strong>{title}</strong>

          <span>
            {items.length} found
          </span>
        </div>
      </div>

      <div className="entity-list">
        {items.length > 0 ? (
          items.map((item) => (
            <div
              className="entity-value"
              key={item.id}
            >
              {item.id}
            </div>
          ))
        ) : (
          <span className="entity-empty">
            None found
          </span>
        )}
      </div>

      {connectedItems?.length > 0 && (
        <div className="shared-warning">
          <span>!</span>

          <div>
            <strong>
              {connectedLabel}
            </strong>

            <p>
              {connectedItems
                .map((item) => item.id)
                .join(", ")}
            </p>
          </div>
        </div>
      )}
    </div>
  );
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

function formatTimestamp(timestamp) {
  if (!timestamp) {
    return "N/A";
  }

  const date = new Date(timestamp);

  if (Number.isNaN(date.getTime())) {
    return "N/A";
  }

  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

export default InvestigationPanel;