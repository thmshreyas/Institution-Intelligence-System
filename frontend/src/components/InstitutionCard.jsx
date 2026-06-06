import { useNavigate } from "react-router-dom";
import ConfidenceBadge from "./ConfidenceBadge";

export default function InstitutionCard({ institution }) {
  const navigate = useNavigate();

  return (
    <button
      type="button"
      onClick={() => navigate(`/institutions/${encodeURIComponent(institution.name)}`)}
      className="group w-full rounded-2xl border border-slate-200 bg-white p-6 text-left shadow-sm transition hover:-translate-y-0.5 hover:border-indigo-300 hover:shadow-md"
    >
      <div className="mb-4 flex items-start justify-between gap-3">
        <div>
          <h3 className="text-lg font-semibold text-slate-900 group-hover:text-indigo-700">
            {institution.name}
          </h3>
          <p className="mt-1 text-sm text-slate-500">{institution.state}</p>
        </div>
        <ConfidenceBadge score={institution.confidence} />
      </div>

      <div className="flex items-center justify-between">
        <span className="text-xs font-medium uppercase tracking-wide text-slate-400">
          View Report
        </span>
        <span className="rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700">
          Open
        </span>
      </div>
    </button>
  );
}
