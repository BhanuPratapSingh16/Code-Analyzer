import "./App.css";
import AuthPage from "./pages/AuthPage";
import { BrowserRouter, Routes, Route, useNavigate, data } from "react-router-dom";
import Navbar from "./components/Navbar";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./routes/ProtectedRoute";

function App() {

  return (
        <Routes>
          <Route path="/" element={<AuthPage />} />

          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard"
              element={
                <>
                  Welcome!
                </>
              }
            />
          </Route>
        </Routes>
  )
}

export default App;
