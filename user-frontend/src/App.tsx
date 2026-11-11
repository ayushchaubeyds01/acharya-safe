
import { useState } from 'react'
import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
  useNavigate,
} from 'react-router-dom'

import './App.css'

import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import EmergencyContacts from './pages/EmergencyContacts'

import Navbar from './components/Navbar'
import { useAuth } from './context/AuthContext'

function AppContent() {
  const { user, loading, logout } = useAuth()
  const [logoutError, setLogoutError] = useState('')
  const navigate = useNavigate()

  async function handleLogout() {
    setLogoutError('')

    try {
      await logout()
      navigate('/login', { replace: true })
    } catch {
      setLogoutError('Logout request failed. Please try again.')
    }
  }

  if (loading) {
    return <main>Checking your session...</main>
  }

  if (!user) {
    return (
      <Routes>
        <Route
          path="/register"
          element={
            <Register
              onLoginClick={() => navigate('/login')}
            />
          }
        />

        <Route
          path="*"
          element={
            <main>
              <Login />
              <p>
                Don't have an account?{' '}
                <button
                  type="button"
                  onClick={() => navigate('/register')}
                >
                  Create Account
                </button>
              </p>
            </main>
          }
        />
      </Routes>
    )
  }

  return (
    <div className="app-shell">
      <Navbar
        fullName={user.full_name}
        email={user.email}
        onLogout={handleLogout}
      />

      <main className="dashboard-content">
        {logoutError && <p role="alert">{logoutError}</p>}

        <Routes>
          <Route
            path="/"
            element={<Navigate to="/dashboard" replace />}
          />

          <Route
            path="/dashboard"
            element={<Dashboard fullName={user.full_name} />}
          />

          <Route
            path="/emergency-contacts"
            element={<EmergencyContacts />}
          />

          <Route
            path="*"
            element={<Navigate to="/dashboard" replace />}
          />
        </Routes>
      </main>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  )
}

export default App