import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import "../../styles/Dashboard.css";

export default function Sidebar({ open, onClose }) {
    const { logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            await logout();
            navigate("/");
        } catch (error) {
            console.error("Logout failed:", error);
        }
    };

    const navItems = [
        { label: "Dashboard", path: "/dashboard", icon: "▦" },
        { label: "My Repositories", path: "/repos", icon: "◈" },
        { label: "Settings", path: "/settings", icon: "⚙" },
    ];

    return (
        <>
            {open && (
                <div className="sidebar-overlay" onClick={onClose} />
            )}

            <aside className={`sidebar ${open ? "sidebar-open" : ""}`}>
                <div className="sidebar-brand">
                    <div className="brand-icon">C</div>
                    <span>CodeGraph<span className="brand-ai"> AI</span></span>
                </div>

                <div className="sidebar-section">
                    <p className="sidebar-heading">WORKSPACE</p>

                    <nav className="sidebar-nav">
                        {navItems.map((item) => (
                            <NavLink
                                key={item.path}
                                to={item.path}
                                end={item.path === "/dashboard"}
                                onClick={onClose}
                                className={({ isActive }) =>
                                    `sidebar-link ${isActive ? "active" : ""}`
                                }
                            >
                                <span className="nav-icon">{item.icon}</span>
                                <span>{item.label}</span>
                            </NavLink>
                        ))}
                    </nav>
                </div>

                <div className="sidebar-bottom">
                    <div className="sidebar-help">
                        <div className="help-icon">?</div>
                        <div>
                            <p>Need help?</p>
                            <span>Contact our support</span>
                        </div>
                    </div>

                    <button className="sidebar-logout" onClick={handleLogout}>
                        <span>↪</span>
                        Logout
                    </button>
                </div>
            </aside>
        </>
    );
}