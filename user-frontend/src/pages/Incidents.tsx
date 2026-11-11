
import { useEffect, useState } from 'react'

import { useAuth } from '../context/AuthContext'
import {
  getIncidents,
  type Incident,
} from '../services/incidents'

import './Incidents.css'

function formatDate(date: string): string {
  return new Date(date).toLocaleString()
}

function formatLabel(value: string): string {
  return value.replaceAll('_', ' ').replace(/\b\w/g, (letter) =>
    letter.toUpperCase()
  )
}

export default function Incidents() {
  const { accessToken } = useAuth()

  const [incidents, setIncidents] = useState<Incident[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let isMounted = true

    async function loadIncidents() {
      if (!accessToken) {
        setError('Please log in to view your incidents.')
        setLoading(false)
        return
      }

      try {
        setLoading(true)
        setError('')

        const data = await getIncidents(accessToken)

        if (isMounted) {
          setIncidents(data)
        }
      } catch {
        if (isMounted) {
          setError('Unable to load incidents. Please try again.')
        }
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    loadIncidents()

    return () => {
      isMounted = false
    }
  }, [accessToken])

  if (loading) {
    return (
      <div className="incidents-page">
        <p className="incidents-message">Loading incident history...</p>
      </div>
    )
  }

  return (
    <div className="incidents-page">
      <section className="incidents-header">
        <p className="incidents-label">YOUR SAFETY RECORD</p>

        <h1>Incident History</h1>

        <p>
          Review your recorded safety incidents and their current status.
        </p>
      </section>

      {error && (
        <div className="incidents-error" role="alert">
          {error}
        </div>
      )}

      {!error && incidents.length === 0 && (
        <div className="incidents-empty">
          <h2>No incidents recorded</h2>

          <p>
            Your incident history will appear here when an emergency
            event is detected or activated.
          </p>
        </div>
      )}

      {!error && incidents.length > 0 && (
        <section className="incidents-list">
          <div className="incidents-list-header">
            <h2>Recorded Incidents</h2>

            <span>{incidents.length} total</span>
          </div>

          {incidents.map((incident) => (
            <article className="incident-card" key={incident.id}>
              <div className="incident-card-header">
                <div>
                  <span className="incident-date">
                    {formatDate(incident.started_at)}
                  </span>

                  <h3>{formatLabel(incident.activation_source)} Activation</h3>
                </div>

                <span
                  className={`incident-severity severity-${incident.severity}`}
                >
                  {formatLabel(incident.severity)}
                </span>
              </div>

              <p className="incident-description">
                {incident.description || 'No additional description available.'}
              </p>

              <div className="incident-details">
                <span>
                  Status: <strong>{formatLabel(incident.status)}</strong>
                </span>

                {incident.location && (
                  <span>
                    Location: <strong>Recorded</strong>
                  </span>
                )}
              </div>

              {incident.resolved_at && (
                <p className="incident-resolved">
                  Resolved: {formatDate(incident.resolved_at)}
                </p>
              )}
            </article>
          ))}
        </section>
      )}
    </div>
  )
}