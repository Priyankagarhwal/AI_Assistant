import { NavLink } from "react-router-dom";

const linkStyle = {
  display: "block",
  padding: "10px 12px",
  borderRadius: "8px",
  color: "#cbd5e1",
  textDecoration: "none",
  fontSize: "15px",
};

const activeStyle = {
  ...linkStyle,
  backgroundColor: "#334155",
  color: "#ffffff",
  fontWeight: "600",
};

export default function Sidebar() {
  return (
    <aside style={{
      position: "fixed",
      top: 0,
      left: 0,
      width: "256px",
      height: "100vh",
      backgroundColor: "#0f172a",
      color: "white",
      zIndex: 50,
      display: "flex",
      flexDirection: "column",
      overflowY: "auto",
    }}>

      <div style={{
        height: "72px",
        display: "flex",
        alignItems: "center",
        padding: "0 24px",
        borderBottom: "1px solid #1e293b",
        flexShrink: 0,
      }}>
        <h1 style={{ fontSize: "18px", fontWeight: "700", color: "white" }}>
          KnowledgeHub AI
        </h1>
      </div>

      <nav style={{ padding: "16px", display: "flex", flexDirection: "column", gap: "4px" }}>
        {[
          { to: "/", label: "Dashboard" },
          { to: "/workspaces", label: "Workspaces" },
          { to: "/upload", label: "Upload PDF" },
          { to: "/chat", label: "AI Chat" },
          { to: "/history", label: "Chat History" },
          { to: "/summary", label: "AI Summary" },
        ].map(({ to, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === "/"}
            style={({ isActive }) => isActive ? activeStyle : linkStyle}
            onMouseEnter={(e) => { if (!e.currentTarget.style.backgroundColor.includes("334155")) e.currentTarget.style.backgroundColor = "#1e293b"; }}
            onMouseLeave={(e) => { if (!e.currentTarget.style.backgroundColor.includes("334155")) e.currentTarget.style.backgroundColor = "transparent"; }}
          >
            {label}
          </NavLink>
        ))}
      </nav>

    </aside>
  );
}