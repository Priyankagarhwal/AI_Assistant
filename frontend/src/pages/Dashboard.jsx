import { useEffect, useState } from "react";
import DashboardCard from "../components/DashboardCard";
import api from "../api/axios";

export default function Dashboard() {
  const [stats, setStats] = useState({ total_workspaces: 0, total_documents: 0, total_chats: 0 });
  const [workspaces, setWorkspaces] = useState([]);

  useEffect(() => {
    api.get("/dashboard/").then((r) => setStats(r.data));
    api.get("/workspace/").then((r) => setWorkspaces(r.data));
  }, []);

  return (
    <div>
      <h1 className="text-4xl font-bold">Dashboard</h1>
      <p className="text-gray-500 mt-2">Welcome to KnowledgeHub AI</p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
        <DashboardCard title="Workspaces" value={stats.total_workspaces} />
        <DashboardCard title="Documents" value={stats.total_documents} />
        <DashboardCard title="Chats" value={stats.total_chats} />
      </div>

      <div className="bg-white rounded-xl shadow p-6 mt-8">
        <h2 className="text-2xl font-bold">Recent Workspaces</h2>
        {workspaces.length === 0 ? (
          <p className="text-gray-500 mt-3">No workspaces available.</p>
        ) : (
          <ul className="mt-4 space-y-2">
            {workspaces.slice(0, 5).map((ws) => (
              <li key={ws.workspace_id} className="flex justify-between border-b pb-2">
                <span className="font-medium">{ws.name}</span>
                <span className="text-gray-400 text-sm">{ws.description}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
