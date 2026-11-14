import "./App.css";
import AuthPage from "./pages/AuthPage";
import { BrowserRouter, Routes, Route, useNavigate, data } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./routes/ProtectedRoute";
import Dashboard from "./pages/Dashboard";

function App() {

  return (
        <Routes>
          <Route path="/" element={<AuthPage />} />

          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard"
              element={
                <Dashboard/>
              }
            />
          </Route>
        </Routes>
  )
}

export default App;
