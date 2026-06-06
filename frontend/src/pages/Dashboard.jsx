import { useEffect, useMemo, useState } from "react";
import { getInstitutions, runPipeline } from "../services/api";
import InstitutionCard from "../components/InstitutionCard";

export default function Dashboard() {
  const [institutions, setInstitutions] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [pipelineStatus, setPipelineStatus] = useState("");

  const loadInstitutions = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await getInstitutions();
      setInstitutions(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load institutions.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInstitutions();
  }, []);

  const filteredInstitutions = useMemo(() => {
    const query = search.trim().toLowerCase();
    if (!query) return institutions;

    return institutions.filter(
      (item) =>
        item.name.toLowerCase().includes(query) ||
        (item.state || "").toLowerCase().includes(query),
    );
  }, [institutions, search]);

  const handleRunPipeline = async () => {
    setPipelineStatus("Running pipeline...");
    try {
      const response = await runPipeline();
      setPipelineStatus(
        `Pipeline completed. Qualified: ${response.data.qualified_count}`,
      );
      await loadInstitutions();
    } catch (err) {
      setPipelineStatus(
        err.response?.data?.detail || "Pipeline execution failed.",
      );
    }
  };

  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-8 sm:px-6 lg:px-8">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm font-medium uppercase tracking-wider text-indigo-600">
                Higher Education Intelligence
              </p>
              <h1 className="mt-1 text-3xl font-bold text-slate-900">
                Institution Intelligence Platform
              </h1>
              <p className="mt-2 max-w-2xl text-slate-600">
                Browse qualified college reports. Select a college to view its
                AI-refined intelligence report with structured analysis.
              </p>
            </div>
            <button
              type="button"
              onClick={handleRunPipeline}
              className="rounded-xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-700"
            >
              Run Pipeline
            </button>
          </div>

          <div className="relative max-w-xl">
            <input
              type="search"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by institution name or state..."
              className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm shadow-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
            />
          </div>

          {pipelineStatus && (
            <p className="text-sm text-slate-600">{pipelineStatus}</p>
          )}
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {loading && (
          <div className="rounded-2xl border border-slate-200 bg-white p-10 text-center text-slate-500">
            Loading institutions...
          </div>
        )}

        {!loading && error && (
          <div className="rounded-2xl border border-rose-200 bg-rose-50 p-6 text-rose-700">
            {error}
          </div>
        )}

        {!loading && !error && filteredInstitutions.length === 0 && (
          <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center text-slate-500">
            No college reports found. Run the pipeline to generate reports.
          </div>
        )}

        {!loading && !error && filteredInstitutions.length > 0 && (
          <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-3">
            {filteredInstitutions.map((institution) => (
              <InstitutionCard
                key={institution.name}
                institution={institution}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
