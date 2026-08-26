import RiskBadge from "./RiskBadge";

function InvestigationPanel({ investigation, onClose }) {
  if (!investigation) {
    return null;
  }

  const {
    transaction,
    account,
    customer,
    merchant,
    devices,
    ip_addresses,
    connected_accounts,
    connected_ip_accounts,
    risk_assessment,
  } = investigation;

  return (
    <div className="investigation-overlay">
      <div className="investigation-panel">

        <div className="panel-header">
          <div>
            <span className="eyebrow">
              FRAUD INVESTIGATION
            </span>

            <h2>{transaction?.id}</h2>
          </div>

          <button
            className="close-button"
            onClick={onClose}
          >
            ×
          </button>
        </div>

        <div className="risk-summary">
          <div>
            <span>Risk Score</span>
            <strong>
              {risk_assessment?.score ?? 0}
            </strong>
          </div>

          <RiskBadge
            level={risk_assessment?.level || "LOW"}
          />
        </div>

        <section>
          <h3>Transaction Context</h3>

          <div className="detail-grid">
            <div>
              <span>Amount</span>
              <strong>
                {transaction?.currency || "USD"}{" "}
                {Number(
                  transaction?.amount || 0
                ).toLocaleString()}
              </strong>
            </div>

            <div>
              <span>Account</span>
              <strong>
                {account?.id || "N/A"}
              </strong>
            </div>

            <div>
              <span>Customer</span>
              <strong>
                {customer?.id || "N/A"}
              </strong>
            </div>

            <div>
              <span>Merchant</span>
              <strong>
                {merchant?.name ||
                  merchant?.id ||
                  "N/A"}
              </strong>
            </div>
          </div>
        </section>

        <section>
          <h3>Connected Entities</h3>

          <div className="entity-grid">

            <div className="entity-card">
              <span>Devices</span>

              {devices?.length > 0 ? (
                devices.map((device) => (
                  <strong key={device.id}>
                    {device.id}
                  </strong>
                ))
              ) : (
                <span>None found</span>
              )}

              {connected_accounts?.length > 0 && (
                <p className="warning-text">
                  ⚠ Shared with{" "}
                  {connected_accounts
                    .map((item) => item.id)
                    .join(", ")}
                </p>
              )}
            </div>

            <div className="entity-card">
              <span>IP Addresses</span>

              {ip_addresses?.length > 0 ? (
                ip_addresses.map((ip) => (
                  <strong key={ip.id}>
                    {ip.id}
                  </strong>
                ))
              ) : (
                <span>None found</span>
              )}

              {connected_ip_accounts?.length > 0 && (
                <p className="warning-text">
                  ⚠ Shared with{" "}
                  {connected_ip_accounts
                    .map((item) => item.id)
                    .join(", ")}
                </p>
              )}
            </div>

          </div>
        </section>

        <section>
          <h3>Risk Indicators</h3>

          <div className="indicator-list">
            {risk_assessment?.indicators?.length > 0 ? (
              risk_assessment.indicators.map(
                (indicator) => (
                  <div
                    className="indicator"
                    key={indicator.code}
                  >
                    <strong>
                      {indicator.code.replaceAll(
                        "_",
                        " "
                      )}
                    </strong>

                    <span>
                      {indicator.description}
                    </span>
                  </div>
                )
              )
            ) : (
              <p>
                No suspicious indicators found.
              </p>
            )}
          </div>
        </section>

      </div>
    </div>
  );
}

export default InvestigationPanel;