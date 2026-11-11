
import { useState } from 'react'
import { NavLink, Link } from 'react-router-dom'

interface NavbarProps {
  fullName: string
  email: string
  onLogout: () => void
}

const navigationItems = [
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'Emergency Contacts', to: '/emergency-contacts' },
  { label: 'Incidents', to: '/incidents' },
  { label: 'My Profile', to: '/profile' },
]

export default function Navbar({
  fullName,
  email,
  onLogout,
}: NavbarProps) {
  const [menuOpen, setMenuOpen] = useState(false)
  const [profileOpen, setProfileOpen] = useState(false)

  const initials = fullName
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part.charAt(0).toUpperCase())
    .join('')

  function closeMenus() {
    setMenuOpen(false)
    setProfileOpen(false)
  }

  return (
    <header className="site-header">
      <nav className="navbar" aria-label="Main navigation">
        <Link
          to="/dashboard"
          className="navbar-brand"
          onClick={closeMenus}
        >
          <span className="brand-icon" aria-hidden="true">
            <svg
              viewBox="0 0 40 40"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M20 3.5L34 9V18.5C34 27.2 28.2 33.2 20 37C11.8 33.2 6 27.2 6 18.5V9L20 3.5Z"
                fill="currentColor"
              />
              <path
                d="M20 10L27 12.8V19C27 24.1 24.2 27.7 20 30C15.8 27.7 13 24.1 13 19V12.8L20 10Z"
                fill="white"
                fillOpacity="0.95"
              />
              <path
                d="M16.5 19.5L19 22L24 16.5"
                stroke="#0F766E"
                strokeWidth="2.2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </span>

          <span className="brand-name">
            ACHARYA <span>SAFE</span>
          </span>
        </Link>

        <button
          type="button"
          className="mobile-menu-button"
          aria-label={menuOpen ? 'Close navigation menu' : 'Open navigation menu'}
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen((open) => !open)}
        >
          <span />
          <span />
          <span />
        </button>

        <div className={`navbar-content ${menuOpen ? 'menu-open' : ''}`}>
          <div className="navbar-links">
            {navigationItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `nav-link ${isActive ? 'active' : ''}`
                }
                onClick={closeMenus}
              >
                {item.label}
              </NavLink>
            ))}
          </div>

          <div className="navbar-actions">
            <div className="profile-wrapper">
              <button
                type="button"
                className="profile-button"
                aria-expanded={profileOpen}
                aria-label="Open profile menu"
                onClick={() => {
                  setProfileOpen((open) => !open)
                  setMenuOpen(false)
                }}
              >
                <span className="profile-avatar">
                  {initials || 'U'}
                </span>

                <span className="profile-name">{fullName}</span>

                <svg
                  className={`profile-chevron ${profileOpen ? 'rotated' : ''}`}
                  viewBox="0 0 20 20"
                  fill="none"
                  aria-hidden="true"
                >
                  <path
                    d="M5 7.5L10 12.5L15 7.5"
                    stroke="currentColor"
                    strokeWidth="1.7"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </button>

              {profileOpen && (
                <div className="profile-dropdown">
                  <div className="profile-dropdown-info">
                    <strong>{fullName}</strong>
                    <span>{email}</span>
                  </div>

                  <div className="dropdown-divider" />

                  <Link to="/profile" onClick={closeMenus}>
                    My Profile
                  </Link>

                  <button
                    type="button"
                    className="logout-button"
                    onClick={() => {
                      closeMenus()
                      onLogout()
                    }}
                  >
                    Sign Out
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </nav>
    </header>
  )
}
