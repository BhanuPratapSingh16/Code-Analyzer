import { useNavigate } from "react-router-dom";
import { logout } from "../services/authService";

const Navbar = () => {
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            await logout();
        } finally {
            navigate("/", { replace: true });
        }
    };

    return (
        <nav className="navbar">
            <h2>CodeGraph AI</h2>

            <button onClick={handleLogout}>
                Logout
            </button>
        </nav>
    );
}

export default Navbar;