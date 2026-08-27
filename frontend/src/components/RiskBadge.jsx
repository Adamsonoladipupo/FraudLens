function RiskBadge({ level }) {
  const normalizedLevel = level?.toLowerCase();

  return (
    <span
      className={`risk-badge risk-${normalizedLevel}`}
    >
      {level}
    </span>
  );
}

export default RiskBadge;