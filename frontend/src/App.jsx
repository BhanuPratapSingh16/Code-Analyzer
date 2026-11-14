import "./App.css";
import AuthPage from "./pages/AuthPage";
import { BrowserRouter, Routes, Route, useNavigate, data } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./routes/ProtectedRoute";
import Dashboard from "./pages/Dashboard";
import CreateRepo from "./pages/CreateRepo";
import Repos from "./pages/Repos";
import RepoDetails from "./pages/RepoDetails";

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
            <Route path="/repos"
              element={
                <Repos/>
              }
            />
            <Route path="/repos/new"
              element={
                <CreateRepo/>
              }
            />
            <Route path="/repos/:id"
              element={
                <RepoDetails/>
              }
            />
          </Route>
        </Routes>
  )
}

export default App;
