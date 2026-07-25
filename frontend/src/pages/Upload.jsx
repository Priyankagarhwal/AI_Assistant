import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Upload() {
  const [workspaces, setWorkspaces] = useState([]);
  const [workspaceId, setWorkspaceId] = useState("");
  const [file, setFile] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  useEffect(() => {
    api.get("/workspace/").then((r) => setWorkspaces(r.data));
  }, []);

  useEffect(() => {
    if (workspaceId) {
      api.get(`/documents/${workspaceId}`).then((r) => setDocuments(r.data));
    } else {
      setDocuments([]);
    }
  }, [workspaceId]);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!workspaceId || !file) return setMsg("Select a workspace and a PDF file.");
    setLoading(true);
    setMsg("");
    const form = new FormData();
    form.append("workspace_id", workspaceId);
    form.append("file", file);
    try {
      const r = await api.post("/upload/pdf", form);
      if (r.data.success) {
        setMsg(`Uploaded! ${r.data.chunks_created} chunks created.`);
        setFile(null);
        api.get(`/documents/${workspaceId}`).then((r) => setDocuments(r.data));
      } else {
        setMsg(r.data.message || "Upload failed.");
      }
    } catch {
      setMsg("Upload failed.");
    }
    setLoading(false);
  };

  const handleDelete = async (docId) => {
    if (!confirm("Delete this document?")) return;
    await api.delete(`/documents/${docId}`);
    api.get(`/documents/${workspaceId}`).then((r) => setDocuments(r.data));
  };

  return (
    <div>
      <h1 className="text-4xl font-bold">Upload PDF</h1>

      <form onSubmit={handleUpload} className="bg-white rounded-xl shadow p-6 mt-8 space-y-4">
        <h2 className="text-xl font-bold">Upload Document</h2>

        <select
          className="w-full border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-slate-400"
          value={workspaceId}
          onChange={(e) => setWorkspaceId(e.target.value)}
        >
          <option value="">Select Workspace</option>
          {workspaces.map((ws) => (
            <option key={ws.workspace_id} value={ws.workspace_id}>{ws.name}</option>
          ))}
        </select>

        <input
          type="file"
          accept=".pdf"
          className="w-full border rounded-lg p-3"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button
          type="submit"
          disabled={loading}
          className="bg-slate-900 text-white px-6 py-2 rounded-lg hover:bg-slate-700 disabled:opacity-50"
        >
          {loading ? "Uploading..." : "Upload"}
        </button>
        {msg && <p className="text-sm text-green-600">{msg}</p>}
      </form>

      {workspaceId && (
        <div className="bg-white rounded-xl shadow p-6 mt-6">
          <h2 className="text-xl font-bold mb-4">Documents in Workspace</h2>
          {documents.length === 0 ? (
            <p className="text-gray-500">No documents uploaded yet.</p>
          ) : (
            <ul className="space-y-3">
              {documents.map((doc) => (
                <li key={doc.document_id} className="flex justify-between items-center border-b pb-3">
                  <span className="font-medium">{doc.filename}</span>
                  <button
                    onClick={() => handleDelete(doc.document_id)}
                    className="text-red-500 hover:text-red-700 text-sm"
                  >
                    Delete
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
