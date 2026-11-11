
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

export interface RegisterData {
  full_name: string
  email: string
  phone_number: string
  password: string
}

export interface EmailLoginData {
  email: string
  password: string
}

export interface MobileOTPRequest {
  phone_number: string
}

export interface MobileOTPVerification {
  phone_number: string
  otp: string
}

export async function registerUser(data: RegisterData): Promise<User> {
  return apiRequest<User>('/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
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

export async function requestMobileOTP(
  data: MobileOTPRequest,
): Promise<{ message: string }> {
  return apiRequest<{ message: string }>('/auth/login/mobile/request-otp', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
}

export async function verifyMobileOTP(
  data: MobileOTPVerification,
): Promise<TokenResponse> {
  return apiRequest<TokenResponse>('/auth/login/mobile/verify-otp', {
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