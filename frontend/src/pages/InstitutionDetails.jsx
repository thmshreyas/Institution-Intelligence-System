import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getInstitution } from "../services/api";
import ConfidenceBadge from "../components/ConfidenceBadge";

function StatusPill({ label, value }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
        {label}
      </p>
      <p
        className={`mt-2 text-sm font-semibold ${
          value ? "text-emerald-700" : "text-slate-500"
        }`}
      >
        {value ? "Verified" : "Not Verified"}
      </p>
    </div>
  );
}

function DetailItem({ label, value }) {
  return (
    <div>
      <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
        {label}
      </p>
      <p className="mt-1 text-sm font-medium text-slate-800">
        {value ?? "Not available"}
      </p>
    </div>
  );
}

function ReportSection({ title, content }) {
  if (!content) return null;

  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-900">{title}</h2>
      <p className="mt-3 text-sm leading-7 text-slate-700">{content}</p>
    </section>
  );
}

export default function InstitutionDetails() {
  const { name } = useParams();
  const decodedName = decodeURIComponent(name);
  const [institution, setInstitution] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadInstitution = async () => {
      setLoading(true);
      setError("");
      try {
        const response = await getInstitution(decodedName);
        setInstitution(response.data);
      } catch (err) {
        setError(
          err.response?.data?.detail || "Failed to load institution report.",
        );
      } finally {
        setLoading(false);
      }
    };

    loadInstitution();
  }, [decodedName]);

  if (loading) {
    return (
      <div className="mx-auto max-w-5xl px-4 py-10 text-slate-500">
        Generating institution intelligence report...
      </div>
    );
  }

  if (error) {
    return (
      <div className="mx-auto max-w-5xl px-4 py-10">
        <Link
          to="/"
          className="text-sm font-medium text-indigo-600 hover:text-indigo-700"
        >
          Back to College List
        </Link>
        <div className="mt-4 rounded-2xl border border-rose-200 bg-rose-50 p-6 text-rose-700">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="border-b border-slate-200 bg-white">
        <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6">
          <Link
            to="/"
            className="text-sm font-medium text-indigo-600 hover:text-indigo-700"
          >
            Back to College List
          </Link>

          <div className="mt-4 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <p className="text-sm font-medium uppercase tracking-wider text-indigo-600">
                Intelligence Report
              </p>
              <h1 className="mt-1 text-3xl font-bold text-slate-900">
                {institution.name}
              </h1>
              <p className="mt-2 text-slate-600">{institution.state}</p>
              {institution.website && (
                <a
                  href={institution.website}
                  target="_blank"
                  rel="noreferrer"
                  className="mt-3 inline-block text-sm font-medium text-indigo-600 hover:text-indigo-700"
                >
                  {institution.website}
                </a>
              )}
            </div>
            <ConfidenceBadge score={institution.confidence} />
          </div>
        </div>
      </div>

      <div className="mx-auto max-w-5xl space-y-6 px-4 py-8 sm:px-6">
        <section className="rounded-2xl border border-indigo-100 bg-gradient-to-br from-indigo-50 to-white p-6 shadow-sm">
          <div className="mb-3 flex items-center gap-2">
            <span
              className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wide text-white ${
                institution.generated_by === "gemini"
                  ? "bg-indigo-600"
                  : "bg-slate-500"
              }`}
            >
              {institution.generated_by === "gemini"
                ? "AI Generated"
                : "Report Summary"}
            </span>
            <h2 className="text-lg font-semibold text-slate-900">
              Executive Summary
            </h2>
          </div>
          <p className="text-sm leading-7 text-slate-700">
            {institution.executive_summary || institution.summary}
          </p>
        </section>

        <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <DetailItem label="Established Year" value={institution.established_year} />
          <DetailItem label="Age" value={institution.age ? `${institution.age} years` : null} />
          <DetailItem label="Vice Chancellor" value={institution.vice_chancellor} />
          <DetailItem label="Address" value={institution.address} />
        </section>

        <section>
          <h2 className="mb-4 text-lg font-semibold text-slate-900">
            Program Verification
          </h2>
          <div className="grid gap-4 sm:grid-cols-3">
            <StatusPill label="Engineering" value={institution.engineering} />
            <StatusPill label="MBA" value={institution.mba} />
            <StatusPill label="PhD" value={institution.phd} />
          </div>
        </section>

        <ReportSection title="Institution Overview" content={institution.overview} />
        <ReportSection title="Academic Strengths" content={institution.academic_strengths} />
        <ReportSection title="Engineering Presence" content={institution.engineering_analysis} />
        <ReportSection title="Management Programs" content={institution.management_analysis} />
        <ReportSection title="Doctoral Programs" content={institution.doctoral_analysis} />
        <ReportSection title="Leadership" content={institution.leadership_analysis} />
        <ReportSection title="Confidence Assessment" content={institution.confidence_assessment} />
      </div>
    </div>
  );
}
