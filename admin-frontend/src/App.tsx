
import { useState } from 'react'
import './App.css'
import Login from './pages/Login'
import { useAuth } from './context/AuthContext'

function App() {
  const { user, loading, logout } = useAuth()
  const [logoutError, setLogoutError] = useState('')

  async function handleLogout() {
    setLogoutError('')

    try {
      await logout()
    } catch {
      setLogoutError('Logout request failed. Please try again.')
    }
  }

  if (loading) {
    return <main>Checking administrator session...</main>
  }

  if (!user) {
    return <Login />
  }

  return (
    <main>
      <h1>ACHARYA SAFE</h1>
      <h2>Admin Dashboard</h2>

      <p>Welcome, {user.full_name}</p>
      <p>Role: {user.role}</p>
      <p>You are successfully logged in as an administrator.</p>

      {logoutError && <p role="alert">{logoutError}</p>}

      <button type="button" onClick={handleLogout}>
        Sign Out
      </button>
    </main>
  )
}

export default App