
import { apiRequest } from './api'

export interface User {
  id: string
  full_name: string
  email: string
  phone_number: string
  role: string
  is_email_verified: boolean
  is_phone_verified: boolean
  is_active: boolean
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface EmailLoginData {
  email: string
  password: string
}

export async function loginWithEmail(
  data: EmailLoginData,
): Promise<TokenResponse> {
  return apiRequest<TokenResponse>('/auth/login/email', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
}

export async function getCurrentUser(token: string): Promise<User> {
  return apiRequest<User>('/auth/me', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
}

export async function refreshAccessToken(): Promise<TokenResponse> {
  return apiRequest<TokenResponse>('/auth/refresh', {
    method: 'POST',
  })
}

export async function logoutUser(): Promise<{ message: string }> {
  return apiRequest<{ message: string }>('/auth/logout', {
    method: 'POST',
  })
}