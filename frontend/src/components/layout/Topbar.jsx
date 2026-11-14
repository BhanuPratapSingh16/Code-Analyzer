import { useAuth } from "../../context/AuthContext";
import { useLocation } from "react-router-dom";
import "../../styles/Dashboard.css";

export default function Topbar({ onMenuClick }) {
    const { user } = useAuth();
    const location = useLocation();

    const getPageTitle = () => {
        if (location.pathname === "/dashboard") return "Dashboard";
        if (location.pathname === "/repos/new") return "Create Repository";
        if (location.pathname.startsWith("/repos/")) return "Repository Workspace";
        if (location.pathname === "/settings") return "Settings";
        return "CodeGraph AI";
    };

    const username =
        typeof user === "string"
            ? user
            : user?.username || user?.name || "Developer";

    return (
        <header className="topbar">
            <div className="topbar-left">
                <button
                    className="menu-button"
                    onClick={onMenuClick}
                    aria-label="Open navigation"
                >
                    ☰
                </button>

                <div>
                    <p className="topbar-breadcrumb">Workspace /</p>
                    <h2>{getPageTitle()}</h2>
                </div>
            </div>

            <div className="topbar-right">
                <div className="topbar-search">
                    <span>⌕</span>
                    <input
                        type="text"
                        placeholder="Search repositories..."
                        aria-label="Search repositories"
                    />
                    <kbd>⌘ K</kbd>
                </div>

                <button className="notification-button" aria-label="Notifications">
                    ♧
                    <span className="notification-dot" />
                </button>

                <div className="topbar-user">
                    <div className="user-avatar">
                        {username.charAt(0).toUpperCase()}
                    </div>

                    <div className="user-info">
                        <p>{username}</p>
                        <span>Developer</span>
                    </div>
                </div>
            </div>
        </header>
    );
}