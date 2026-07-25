export default function Navbar() {
  return (
    <header style={{
      height: "72px",
      backgroundColor: "white",
      borderBottom: "1px solid #e2e8f0",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "0 32px",
      position: "sticky",
      top: 0,
      zIndex: 40,
      flexShrink: 0,
      width: "100%",
    }}>

      <div>
        <h1 style={{ fontSize: "20px", fontWeight: "700", color: "#0f172a" }}>
          KnowledgeHub AI
        </h1>
        <p style={{ fontSize: "13px", color: "#94a3b8" }}>Welcome back 👋</p>
      </div>

      <div style={{ textAlign: "right" }}>
        <p style={{ fontWeight: "600", color: "#0f172a" }}>Priyanka Garhwal</p>
        <p style={{ fontSize: "13px", color: "#94a3b8" }}>AI Assistant</p>
      </div>

    </header>
  );
}