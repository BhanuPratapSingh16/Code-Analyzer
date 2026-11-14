import { useState } from "react";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";
import "../../styles/Dashboard.css";

export default function DashboardLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="dashboard-shell">
      <Sidebar
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      <div className="dashboard-main">
        <Topbar onMenuClick={() => setSidebarOpen(true)} />

        <main className="dashboard-content">
          {children}
        </main>
      </div>
    </div>
  );
}