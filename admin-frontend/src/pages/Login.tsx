
import { useState, type FormEvent } from 'react'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const { loginWithEmail } = useAuth()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setSubmitting(true)

    try {
      await loginWithEmail({ email, password })
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Admin login failed. Please try again.',
      )
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main>
      <h1>ACHARYA SAFE</h1>
      <h2>Administrator Login</h2>
      <p>Sign in to the administration portal</p>

      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="adminEmail">Email Address</label>
          <input
            id="adminEmail"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="Enter administrator email"
            autoComplete="username"
            required
          />
        </div>

        <div>
          <label htmlFor="adminPassword">Password</label>
          <input
            id="adminPassword"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Enter your password"
            autoComplete="current-password"
            required
          />
        </div>

        {error && <p role="alert">{error}</p>}

        <button type="submit" disabled={submitting}>
          {submitting ? 'Signing in...' : 'Admin Sign In'}
        </button>
      </form>
    </main>
  )
}