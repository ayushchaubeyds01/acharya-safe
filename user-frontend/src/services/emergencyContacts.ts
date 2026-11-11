
import { apiRequest } from './api'

export interface EmergencyContact {
  id: string
  name: string
  phone_number: string
  relationship: string
  created_at: string
  updated_at: string
}

export interface EmergencyContactCreate {
  name: string
  phone_number: string
  relationship: string
}

export interface EmergencyContactUpdate {
  name?: string
  phone_number?: string
  relationship?: string
}

export async function getEmergencyContacts(
  token: string,
): Promise<EmergencyContact[]> {
  return apiRequest<EmergencyContact[]>('/emergency-contacts', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
}

export async function createEmergencyContact(
  token: string,
  data: EmergencyContactCreate,
): Promise<EmergencyContact> {
  return apiRequest<EmergencyContact>('/emergency-contacts', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
}

export async function updateEmergencyContact(
  token: string,
  contactId: string,
  data: EmergencyContactUpdate,
): Promise<EmergencyContact> {
  return apiRequest<EmergencyContact>(
    `/emergency-contacts/${contactId}`,
    {
      method: 'PATCH',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    },
  )
}

export async function deleteEmergencyContact(
  token: string,
  contactId: string,
): Promise<void> {
  return apiRequest<void>(`/emergency-contacts/${contactId}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
}