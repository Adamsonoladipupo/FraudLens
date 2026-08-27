function StatCard({
  title,
  value,
  description,
}) {
  return (
    <article className="stat-card">
      <div className="stat-card-header">
        <span className="stat-title">
          {title}
        </span>

        <span className="stat-icon">
          ↗
        </span>
      </div>

      <div className="stat-value">
        {value}
      </div>

      {description && (
        <div className="stat-description">
          {description}
        </div>
      )}
    </article>
  );
}

export default StatCard;