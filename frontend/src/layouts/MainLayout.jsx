import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

export default function MainLayout({ children }) {
  return (
    <div style={{ display: "flex", minHeight: "100vh", backgroundColor: "#f1f5f9" }}>

      <Sidebar />

      <div style={{
        marginLeft: "256px",
        flex: 1,
        minWidth: 0,
        width: "calc(100% - 256px)",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
      }}>

        <Navbar />

        <main style={{ padding: "2rem", flex: 1, overflowY: "auto" }}>
          {children}
        </main>

      </div>

    </div>
  );
}