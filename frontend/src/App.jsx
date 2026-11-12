import "./App.css";
import AuthPage from "./pages/AuthPage";
import { BrowserRouter, Routes, Route, useNavigate, data } from "react-router-dom";
import { login, signup } from "./services/authService";
import Navbar from "./components/Navbar";

function App() {

  const navigate = useNavigate();

  const handleLogin = async (data) => {
    const response = await login(data);

    navigate("/dashboard");
    return response;
  }

  const handleSignup = async (data) => {
    return await signup(data);
  }

  return (
    <>
        <Routes>
          <Route
            path="/"
            element={
              <AuthPage onLogin={handleLogin} onSignup={handleSignup} />
            }
          />
          <Route
            path="/dashboard"
            element={
              <>
                <Navbar />
                <h1>Welcome to CodeGraph AI</h1>
              </>
            }
          />
        </Routes>
    </>
  )
}

export default App;
