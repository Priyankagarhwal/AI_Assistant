import { useEffect, useState } from "react";
import api from "../api/axios";

export default function History() {
  const [workspaces, setWorkspaces] = useState([]);
  const [workspaceId, setWorkspaceId] = useState("");
  const [history, setHistory] = useState([]);

  useEffect(() => {
    api.get("/workspace/").then((r) => setWorkspaces(r.data));
  }, []);

  useEffect(() => {
    if (workspaceId) {
      api.get(`/chat/history/${workspaceId}`).then((r) => setHistory(r.data));
    } else {
      setHistory([]);
    }
  }, [workspaceId]);

  return (
    <div>
      <h1 className="text-4xl font-bold">Chat History</h1>

      <div className="bg-white rounded-xl shadow p-4 mt-6">
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
      </div>

      <div className="bg-white rounded-xl shadow p-6 mt-4 space-y-6">
        {history.length === 0 ? (
          <p className="text-gray-500">
            {workspaceId ? "No chat history for this workspace." : "Select a workspace to view history."}
          </p>
        ) : (
          history.map((item) => (
            <div key={item.chat_id} className="border-b pb-4">
              <p className="font-semibold text-slate-800">Q: {item.question}</p>
              <p className="text-slate-600 mt-1 text-sm whitespace-pre-wrap">A: {item.answer}</p>
              <p className="text-gray-400 text-xs mt-2">
                {new Date(item.created_at).toLocaleString()}
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
