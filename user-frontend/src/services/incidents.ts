
import { apiRequest } from './api'

export type ActivationSource = 'voice' | 'movement' | 'manual'

export type IncidentSeverity =
  | 'critical'
  | 'high'
  | 'medium'
  | 'low'
  | 'unknown'

export type IncidentStatus =
  | 'detected'
  | 'investigating'
  | 'responding'
  | 'resolved'
  | 'false_alarm'

export interface IncidentLocation {
  latitude?: number
  longitude?: number
  accuracy?: number
}

export interface Incident {
  id: string
  user_id: string
  activation_source: ActivationSource
  severity: IncidentSeverity
  status: IncidentStatus
  description: string | null
  location: IncidentLocation | null
  started_at: string
  resolved_at: string | null
  created_at: string
  updated_at: string
}

export async function getIncidents(
  token: string,
): Promise<Incident[]> {
  return apiRequest<Incident[]>('/incidents', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
}

export async function getIncidentById(
  token: string,
  incidentId: string,
): Promise<Incident> {
  return apiRequest<Incident>(`/incidents/${incidentId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
}
