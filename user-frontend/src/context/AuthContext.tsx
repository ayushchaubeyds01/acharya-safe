
import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from 'react'

import {
  getCurrentUser,
  loginWithEmail as loginWithEmailRequest,
  logoutUser as logoutRequest,
  refreshAccessToken,
  verifyMobileOTP as verifyMobileOTPRequest,
  type EmailLoginData,
  type MobileOTPVerification,
  type TokenResponse,
  type User,
} from '../services/auth'

interface AuthContextType {
  user: User | null
  accessToken: string | null
  loading: boolean
  loginWithEmail: (data: EmailLoginData) => Promise<void>
  verifyMobileOTP: (data: MobileOTPVerification) => Promise<void>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

let sessionRestorePromise: Promise<TokenResponse | null> | null = null

function restoreSession(): Promise<TokenResponse | null> {
  if (!sessionRestorePromise) {
    sessionRestorePromise = refreshAccessToken().catch(() => {
      sessionRestorePromise = null
      return null
    })
  }

  return sessionRestorePromise
}

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const [accessToken, setAccessToken] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let isMounted = true

    async function initializeAuth() {
      try {
        const tokenResponse = await restoreSession()

        if (!tokenResponse) {
          return
        }

        const currentUser = await getCurrentUser(
          tokenResponse.access_token,
        )

        if (isMounted) {
          setAccessToken(tokenResponse.access_token)
          setUser(currentUser)
        }
      } catch {
        if (isMounted) {
          setAccessToken(null)
          setUser(null)
        }
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    initializeAuth()

    return () => {
      isMounted = false
    }
  }, [])

  async function loginWithEmail(data: EmailLoginData): Promise<void> {
    const tokenResponse = await loginWithEmailRequest(data)

    const currentUser = await getCurrentUser(
      tokenResponse.access_token,
    )

    setAccessToken(tokenResponse.access_token)
    setUser(currentUser)
  }

  async function verifyMobileOTP(
    data: MobileOTPVerification,
  ): Promise<void> {
    const tokenResponse = await verifyMobileOTPRequest(data)

    const currentUser = await getCurrentUser(
      tokenResponse.access_token,
    )

    setAccessToken(tokenResponse.access_token)
    setUser(currentUser)
  }

  async function logout(): Promise<void> {
    try {
      await logoutRequest()
    } finally {
      setAccessToken(null)
      setUser(null)
      sessionRestorePromise = null
    }
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        accessToken,
        loading,
        loginWithEmail,
        verifyMobileOTP,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }

  return context
}