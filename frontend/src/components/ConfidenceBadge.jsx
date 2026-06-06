function getBadgeStyles(score) {
  if (score >= 80) {
    return "bg-emerald-100 text-emerald-800 ring-emerald-200";
  }
  if (score >= 60) {
    return "bg-amber-100 text-amber-800 ring-amber-200";
  }
  return "bg-rose-100 text-rose-800 ring-rose-200";
}

export default function ConfidenceBadge({ score }) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-3 py-1 text-sm font-semibold ring-1 ring-inset ${getBadgeStyles(score)}`}
    >
      {score}/100
    </span>
  );
}
