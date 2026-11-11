
import { useState, type FormEvent } from 'react'
import { useAuth } from '../context/AuthContext'
import { requestMobileOTP } from '../services/auth'

export default function Login() {
  const { loginWithEmail, verifyMobileOTP } = useAuth()

  const [loginMode, setLoginMode] = useState<'email' | 'mobile'>('email')

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const [phoneNumber, setPhoneNumber] = useState('')
  const [otp, setOtp] = useState('')
  const [otpSent, setOtpSent] = useState(false)

  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleEmailLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setMessage('')
    setSubmitting(true)

    try {
      await loginWithEmail({ email, password })
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Login failed. Please try again.',
      )
    } finally {
      setSubmitting(false)
    }
  }

  async function handleMobileLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setMessage('')
    setSubmitting(true)

    try {
      if (!otpSent) {
        const response = await requestMobileOTP({
          phone_number: phoneNumber,
        })

        setOtpSent(true)
        setMessage(response.message)
      } else {
        await verifyMobileOTP({
          phone_number: phoneNumber,
          otp,
        })
      }
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Mobile login failed. Please try again.',
      )
    } finally {
      setSubmitting(false)
    }
  }

  function changeLoginMode(mode: 'email' | 'mobile') {
    setLoginMode(mode)
    setError('')
    setMessage('')
    setOtpSent(false)
    setOtp('')
  }

  return (
    <main>
      <h1>ACHARYA SAFE</h1>
      <h2>Welcome Back</h2>
      <p>Sign in to your account</p>

      <div>
        <button
          type="button"
          onClick={() => changeLoginMode('email')}
          disabled={loginMode === 'email'}
        >
          Email Login
        </button>

        <button
          type="button"
          onClick={() => changeLoginMode('mobile')}
          disabled={loginMode === 'mobile'}
        >
          Mobile OTP Login
        </button>
      </div>

      {loginMode === 'email' ? (
        <form onSubmit={handleEmailLogin}>
          <div>
            <label htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="Enter your email"
              autoComplete="email"
              required
            />
          </div>

          <div>
            <label htmlFor="password">Password</label>
            <input
              id="password"
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
            {submitting ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
      ) : (
        <form onSubmit={handleMobileLogin}>
          <div>
            <label htmlFor="phoneNumber">Phone Number</label>
            <input
              id="phoneNumber"
              type="tel"
              value={phoneNumber}
              onChange={(event) => {
                setPhoneNumber(event.target.value)
                setOtpSent(false)
                setOtp('')
                setMessage('')
                setError('')
              }}
              placeholder="Enter your registered phone number"
              autoComplete="tel"
              minLength={10}
              maxLength={20}
              required
            />
          </div>

          {otpSent && (
            <div>
              <label htmlFor="otp">Enter OTP</label>
              <input
                id="otp"
                type="text"
                value={otp}
                onChange={(event) => setOtp(event.target.value)}
                placeholder="Enter 6-digit OTP"
                inputMode="numeric"
                pattern="[0-9]{6}"
                maxLength={6}
                required
              />
            </div>
          )}

          {message && <p role="status">{message}</p>}
          {error && <p role="alert">{error}</p>}

          <button type="submit" disabled={submitting}>
            {submitting
              ? 'Please wait...'
              : otpSent
                ? 'Verify OTP'
                : 'Send OTP'}
          </button>
        </form>
      )}
    </main>
  )
}