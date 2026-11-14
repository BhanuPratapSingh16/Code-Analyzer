import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import Navbar from '../components/Navbar';

const ProtectedRoute = () => {
  const { user, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return <div>Loading...</div>
  }

  if (!user) {
    return <Navigate to="/" state={{from:location}} replace/>
  }

  return (
    <>
      <main>
        <Outlet/>
      </main>
    </>
  )
}

export default ProtectedRoute