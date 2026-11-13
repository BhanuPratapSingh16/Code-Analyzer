import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./Navbar.css";

const Navbar = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const [isLoggingOut, setIsLoggingOut] = useState(false);

    const handleLogout = async () => {
        try {
            setIsLoggingOut(true);
            await logout();
            navigate("/", { replace: true });
        } catch (error) {
            console.error("Logout failed:", error);
        } finally {
            setIsLoggingOut(false);
        }
    };

    return (
        <nav className="navbar">
            <div className="navbar-left">
                <Link to="/dashboard" className="navbar-brand">
                    <div className="brand-logo">CG</div>
                    <span>
                        CodeGraph<strong>AI</strong>
                    </span>
                </Link>
            </div>

            <div className="navbar-right">
                {user && (
                    <>
                        <span className="navbar-user">@{user.username}</span>
                        <button
                            type="button"
                            className="logout-btn"
                            onClick={handleLogout}
                            disabled={isLoggingOut}
                        >
                            {isLoggingOut ? "Logging out..." : "Logout"}
                        </button>
                    </>
                )}
            </div>
        </nav>
    );
};

export default Navbar;
