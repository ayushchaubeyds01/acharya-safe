
import { useState } from 'react'
import './App.css'
import Login from './pages/Login'
import Register from './pages/Register'
import { useAuth } from './context/AuthContext'

function App() {
  const { user, loading, logout } = useAuth()
  const [logoutError, setLogoutError] = useState('')
  const [showRegister, setShowRegister] = useState(false)

  async function handleLogout() {
    setLogoutError('')

    try {
      await logout()
    } catch {
      setLogoutError('Logout request failed. Please try again.')
    }
  }

  if (loading) {
    return <main>Checking your session...</main>
  }

  if (!user) {
    if (showRegister) {
      return (
        <Register
          onLoginClick={() => setShowRegister(false)}
        />
      )
    }

    return (
      <main>
        <Login />
        <p>
          Don't have an account?{' '}
          <button
            type="button"
            onClick={() => setShowRegister(true)}
          >
            Create Account
          </button>
        </p>
      </main>
    )
  }

  return (
    <main>
      <h1>ACHARYA SAFE</h1>
      <h2>Welcome, {user.full_name}</h2>
      <p>You are successfully logged in.</p>

      {logoutError && <p role="alert">{logoutError}</p>}

      <button type="button" onClick={handleLogout}>
        Sign Out
      </button>
    </main>
  )
}

export default App