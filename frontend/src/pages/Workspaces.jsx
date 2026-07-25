import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Workspaces() {
  const [workspaces, setWorkspaces] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const fetchWorkspaces = () => api.get("/workspace/").then((r) => setWorkspaces(r.data));

  useEffect(() => { fetchWorkspaces(); }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    setLoading(true);
    setMsg("");
    try {
      await api.post("/workspace/", { name, description });
      setName("");
      setDescription("");
      setMsg("Workspace created!");
      fetchWorkspaces();
    } catch {
      setMsg("Failed to create workspace.");
    }
    setLoading(false);
  };

  const handleDelete = async (id) => {
    if (!confirm("Delete this workspace?")) return;
    await api.delete(`/workspace/${id}`);
    fetchWorkspaces();
  };

  return (
    <div>
      <h1 className="text-4xl font-bold">Workspaces</h1>

      <form onSubmit={handleCreate} className="bg-white rounded-xl shadow p-6 mt-8 space-y-4">
        <h2 className="text-xl font-bold">Create Workspace</h2>
        <input
          className="w-full border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-slate-400"
          placeholder="Workspace name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          className="w-full border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-slate-400"
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-slate-900 text-white px-6 py-2 rounded-lg hover:bg-slate-700 disabled:opacity-50"
        >
          {loading ? "Creating..." : "Create"}
        </button>
        {msg && <p className="text-sm text-green-600">{msg}</p>}
      </form>

      <div className="bg-white rounded-xl shadow p-6 mt-6">
        <h2 className="text-xl font-bold mb-4">All Workspaces</h2>
        {workspaces.length === 0 ? (
          <p className="text-gray-500">No workspaces yet.</p>
        ) : (
          <ul className="space-y-3">
            {workspaces.map((ws) => (
              <li key={ws.workspace_id} className="flex justify-between items-center border-b pb-3">
                <div>
                  <p className="font-semibold">{ws.name}</p>
                  <p className="text-gray-400 text-sm">{ws.description}</p>
                </div>
                <button
                  onClick={() => handleDelete(ws.workspace_id)}
                  className="text-red-500 hover:text-red-700 text-sm"
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
