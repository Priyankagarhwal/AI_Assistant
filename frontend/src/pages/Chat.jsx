import { useEffect, useState } from "react";
import api, { errorMessage } from "../api/axios";

// Build [{question, answer}] pairs from the visible conversation so the backend
// can resolve follow-up questions ("what about its limitations?").
function toHistory(messages) {
  const turns = [];
  for (let i = 0; i < messages.length - 1; i++) {
    if (messages[i].role === "user" && messages[i + 1].role === "ai" && !messages[i + 1].error) {
      turns.push({ question: messages[i].text, answer: messages[i + 1].text });
    }
  }
  return turns.slice(-4);
}

export default function Chat() {
  const [workspaces, setWorkspaces] = useState([]);
  const [workspaceId, setWorkspaceId] = useState("");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.get("/workspace/").then((r) => setWorkspaces(r.data));
  }, []);

  const handleAsk = async (e) => {
    e.preventDefault();
    if (!workspaceId || !question.trim()) return;
    const q = question.trim();
    const history = toHistory(messages);
    setMessages((prev) => [...prev, { role: "user", text: q }]);
    setQuestion("");
    setLoading(true);
    try {
      const r = await api.post("/chat/", { workspace_id: workspaceId, question: q, history });
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: r.data.answer, sources: r.data.sources },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "ai", error: true, text: errorMessage(err, "Error getting response.") },
      ]);
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col h-full">
      <h1 className="text-4xl font-bold">AI Chat</h1>

      <div className="bg-white rounded-xl shadow p-4 mt-6">
        <select
          className="w-full border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-slate-400"
          value={workspaceId}
          onChange={(e) => { setWorkspaceId(e.target.value); setMessages([]); }}
        >
          <option value="">Select Workspace</option>
          {workspaces.map((ws) => (
            <option key={ws.workspace_id} value={ws.workspace_id}>{ws.name}</option>
          ))}
        </select>
      </div>

      <div className="bg-white rounded-xl shadow p-6 mt-4 flex-1 min-h-64 space-y-4 overflow-y-auto">
        {messages.length === 0 && (
          <p className="text-gray-400 text-center mt-8">Select a workspace and ask a question.</p>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-2xl rounded-xl px-4 py-3 text-sm whitespace-pre-wrap ${
                m.role === "user"
                  ? "bg-slate-900 text-white"
                  : "bg-slate-100 text-slate-800"
              }`}
            >
              {m.text}
              {m.sources && m.sources.length > 0 && (
                <ul className="mt-2 space-y-1 text-xs text-slate-500">
                  {m.sources.map((s) => (
                    <li key={s.id} title={s.snippet}>
                      [{s.id}] {s.filename}, p. {s.page}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-slate-100 rounded-xl px-4 py-3 text-sm text-slate-500">Thinking...</div>
          </div>
        )}
      </div>

      <form onSubmit={handleAsk} className="flex gap-3 mt-4">
        <input
          className="flex-1 border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-slate-400"
          placeholder="Ask a question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          disabled={!workspaceId || loading}
        />
        <button
          type="submit"
          disabled={!workspaceId || loading || !question.trim()}
          className="bg-slate-900 text-white px-6 py-3 rounded-lg hover:bg-slate-700 disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </div>
  );
}
