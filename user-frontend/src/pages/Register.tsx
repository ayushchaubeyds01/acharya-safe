
import { useState, type FormEvent } from 'react'
import { registerUser } from '../services/auth'

interface RegisterProps {
  onLoginClick: () => void
}

export default function Register({ onLoginClick }: RegisterProps) {
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [phoneNumber, setPhoneNumber] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setSuccess('')

    if (password !== confirmPassword) {
      setError('Passwords do not match.')
      return
    }

    setSubmitting(true)

    try {
      await registerUser({
        full_name: fullName,
        email,
        phone_number: phoneNumber,
        password,
      })

      setSuccess('Account created successfully. You can now sign in.')
      setFullName('')
      setEmail('')
      setPhoneNumber('')
      setPassword('')
      setConfirmPassword('')
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Registration failed. Please try again.',
      )
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main>
      <h1>ACHARYA SAFE</h1>
      <h2>Create Account</h2>
      <p>Register to get started</p>

      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="fullName">Full Name</label>
          <input
            id="fullName"
            type="text"
            value={fullName}
            onChange={(event) => setFullName(event.target.value)}
            placeholder="Enter your full name"
            autoComplete="name"
            minLength={2}
            maxLength={120}
            required
          />
        </div>

        <div>
          <label htmlFor="registerEmail">Email Address</label>
          <input
            id="registerEmail"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="Enter your email"
            autoComplete="email"
            required
          />
        </div>

        <div>
          <label htmlFor="phoneNumber">Phone Number</label>
          <input
            id="phoneNumber"
            type="tel"
            value={phoneNumber}
            onChange={(event) => setPhoneNumber(event.target.value)}
            placeholder="Enter your phone number"
            autoComplete="tel"
            minLength={10}
            maxLength={20}
            required
          />
        </div>

        <div>
          <label htmlFor="registerPassword">Password</label>
          <input
            id="registerPassword"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Create a password"
            autoComplete="new-password"
            minLength={8}
            maxLength={128}
            required
          />
        </div>

        <div>
          <label htmlFor="confirmPassword">Confirm Password</label>
          <input
            id="confirmPassword"
            type="password"
            value={confirmPassword}
            onChange={(event) => setConfirmPassword(event.target.value)}
            placeholder="Confirm your password"
            autoComplete="new-password"
            minLength={8}
            maxLength={128}
            required
          />
        </div>

        {error && <p role="alert">{error}</p>}
        {success && <p role="status">{success}</p>}

        <button type="submit" disabled={submitting}>
          {submitting ? 'Creating Account...' : 'Create Account'}
        </button>
      </form>

      <p>
        Already have an account?{' '}
        <button type="button" onClick={onLoginClick}>
          Sign In
        </button>
      </p>
    </main>
  )
}