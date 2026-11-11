
interface DashboardProps {
  fullName: string
}

export default function Dashboard({ fullName }: DashboardProps) {
  return (
    <div className="dashboard-page">
      <section className="welcome-section">
        <p className="welcome-label">YOUR PERSONAL SAFETY SPACE</p>

        <h1>Welcome back, {fullName}</h1>

        <p>
          Stay prepared, stay connected, and take control of your safety.
        </p>
      </section>

      <section className="emergency-section">
        <div className="emergency-card">
          <div className="emergency-card-content">
            <span className="emergency-status">EMERGENCY ASSISTANCE</span>

            <h2>Need immediate help?</h2>

            <p>
              Emergency activation will be available here once the
              emergency-response system is implemented.
            </p>
          </div>

          <button
            type="button"
            className="emergency-button"
            disabled
          >
            Emergency Activation
          </button>
        </div>
      </section>

      <section className="dashboard-grid">
        <article className="dashboard-card" id="emergency-contacts">
          <div className="dashboard-card-icon contacts-icon">
            <span aria-hidden="true">+</span>
          </div>

          <h3>Emergency Contacts</h3>

          <p>
            Manage the trusted people who can be contacted during
            an emergency.
          </p>

          <span className="feature-status">Available</span>
        </article>

        <article className="dashboard-card" id="incidents">
          <div className="dashboard-card-icon incidents-icon">
            <span aria-hidden="true">!</span>
          </div>

          <h3>Recent Incidents</h3>

          <p>
            Review your emergency history and recorded safety incidents.
          </p>

          <span className="feature-status">Coming soon</span>
        </article>

        <article className="dashboard-card" id="profile">
          <div className="dashboard-card-icon profile-icon">
            <span aria-hidden="true">✓</span>
          </div>

          <h3>Account & Safety</h3>

          <p>
            Your account is active. Additional safety settings will
            be available here.
          </p>

          <span className="feature-status">Account active</span>
        </article>
      </section>
    </div>
  )
}
