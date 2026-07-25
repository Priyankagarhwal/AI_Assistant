import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Summary() {
  const [workspaces, setWorkspaces] = useState([]);
  const [workspaceId, setWorkspaceId] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.get("/workspace/").then((r) => setWorkspaces(r.data));
  }, []);

  const handleGenerate = async () => {
    if (!workspaceId) return;
    setLoading(true);
    setSummary("");
    try {
      const r = await api.post("/summary/", { workspace_id: workspaceId });
      setSummary(r.data.summary);
    } catch {
      setSummary("Failed to generate summary.");
    }
    setLoading(false);
  };

  return (
    <div>
      <h1 className="text-4xl font-bold">AI Summary</h1>

      <div className="bg-white rounded-xl shadow p-6 mt-8 space-y-4">
        <h2 className="text-xl font-bold">Generate Summary</h2>

        <select
          className="w-full border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-slate-400"
          value={workspaceId}
          onChange={(e) => { setWorkspaceId(e.target.value); setSummary(""); }}
        >
          <option value="">Select Workspace</option>
          {workspaces.map((ws) => (
            <option key={ws.workspace_id} value={ws.workspace_id}>{ws.name}</option>
          ))}
        </select>

        <button
          onClick={handleGenerate}
          disabled={!workspaceId || loading}
          className="bg-slate-900 text-white px-6 py-2 rounded-lg hover:bg-slate-700 disabled:opacity-50"
        >
          {loading ? "Generating..." : "Generate Summary"}
        </button>
      </div>

      {summary && (
        <div className="bg-white rounded-xl shadow p-6 mt-6">
          <h2 className="text-xl font-bold mb-4">Summary</h2>
          <p className="text-slate-700 whitespace-pre-wrap text-sm leading-relaxed">{summary}</p>
        </div>
      )}
    </div>
  );
}
