function RiskBadge({ level }) {
  const normalizedLevel = level?.toUpperCase() || "UNKNOWN";

  return (
    <span className={`risk-badge risk-${normalizedLevel.toLowerCase()}`}>
      {normalizedLevel}
    </span>
  );
}

export default RiskBadge;
