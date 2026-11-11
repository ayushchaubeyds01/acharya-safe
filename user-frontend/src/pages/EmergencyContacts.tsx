
import { useEffect, useState, type FormEvent } from 'react'
import { useAuth } from '../context/AuthContext'
import {
  createEmergencyContact,
  deleteEmergencyContact,
  getEmergencyContacts,
  updateEmergencyContact,
  type EmergencyContact,
} from '../services/emergencyContacts'
import './EmergencyContacts.css'

interface ContactFormData {
  name: string
  phone_number: string
  relationship: string
}

const initialFormData: ContactFormData = {
  name: '',
  phone_number: '',
  relationship: '',
}

export default function EmergencyContacts() {
  const { accessToken } = useAuth()

  const [contacts, setContacts] = useState<EmergencyContact[]>([])
  const [formData, setFormData] = useState<ContactFormData>(initialFormData)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  async function loadContacts() {
    if (!accessToken) {
      setLoading(false)
      return
    }

    setError('')

    try {
      const data = await getEmergencyContacts(accessToken)
      setContacts(data)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Unable to load emergency contacts.',
      )
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadContacts()
  }, [accessToken])

  function handleInputChange(
    event: React.ChangeEvent<HTMLInputElement>,
  ) {
    const { name, value } = event.target

    setFormData((current) => ({
      ...current,
      [name]: value,
    }))
  }

  function resetForm() {
    setFormData(initialFormData)
    setEditingId(null)
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    if (!accessToken) {
      setError('Your session has expired. Please sign in again.')
      return
    }

    setSaving(true)
    setError('')
    setSuccess('')

    try {
      if (editingId) {
        await updateEmergencyContact(accessToken, editingId, formData)
        setSuccess('Emergency contact updated successfully.')
      } else {
        await createEmergencyContact(accessToken, formData)
        setSuccess('Emergency contact added successfully.')
      }

      resetForm()
      await loadContacts()
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Unable to save emergency contact.',
      )
    } finally {
      setSaving(false)
    }
  }

  function handleEdit(contact: EmergencyContact) {
    setEditingId(contact.id)

    setFormData({
      name: contact.name,
      phone_number: contact.phone_number,
      relationship: contact.relationship,
    })

    setError('')
    setSuccess('')
  }

  async function handleDelete(contactId: string) {
    if (!accessToken) {
      setError('Your session has expired. Please sign in again.')
      return
    }

    const confirmed = window.confirm(
      'Are you sure you want to delete this emergency contact?',
    )

    if (!confirmed) {
      return
    }

    setError('')
    setSuccess('')

    try {
      await deleteEmergencyContact(accessToken, contactId)

      if (editingId === contactId) {
        resetForm()
      }

      setSuccess('Emergency contact deleted successfully.')
      await loadContacts()
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Unable to delete emergency contact.',
      )
    }
  }

  return (
    <section className="contacts-section">
      <div className="contacts-section-heading">
        <div>
          <p className="contacts-eyebrow">YOUR TRUSTED NETWORK</p>
          <h2>Emergency Contacts</h2>
          <p>
            Add and manage the people you trust to contact during
            an emergency.
          </p>
        </div>

        <span className="contacts-count">
          {contacts.length} {contacts.length === 1 ? 'Contact' : 'Contacts'}
        </span>
      </div>

      {error && (
        <p className="contacts-message error-message" role="alert">
          {error}
        </p>
      )}

      {success && (
        <p className="contacts-message success-message" role="status">
          {success}
        </p>
      )}

      <div className="contacts-layout">
        <div className="contacts-list-panel">
          <h3>Your Trusted Contacts</h3>

          {loading ? (
            <p className="contacts-empty">Loading contacts...</p>
          ) : contacts.length === 0 ? (
            <div className="contacts-empty">
              <h4>No emergency contacts yet</h4>
              <p>
                Add someone you trust so they can be part of your
                emergency support network.
              </p>
            </div>
          ) : (
            <div className="contacts-list">
              {contacts.map((contact) => (
                <article className="contact-item" key={contact.id}>
                  <div className="contact-avatar" aria-hidden="true">
                    {contact.name.charAt(0).toUpperCase()}
                  </div>

                  <div className="contact-details">
                    <h4>{contact.name}</h4>
                    <p>{contact.phone_number}</p>
                    <span>{contact.relationship}</span>
                  </div>

                  <div className="contact-actions">
                    <button
                      type="button"
                      className="contact-edit-button"
                      onClick={() => handleEdit(contact)}
                    >
                      Edit
                    </button>

                    <button
                      type="button"
                      className="contact-delete-button"
                      onClick={() => handleDelete(contact.id)}
                    >
                      Delete
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </div>

        <div className="contact-form-panel">
          <h3>{editingId ? 'Edit Contact' : 'Add New Contact'}</h3>

          <form onSubmit={handleSubmit}>
            <label htmlFor="contact-name">Full Name</label>
            <input
              id="contact-name"
              name="name"
              type="text"
              placeholder="Enter contact's full name"
              value={formData.name}
              onChange={handleInputChange}
              maxLength={120}
              required
            />

            <label htmlFor="contact-phone">Phone Number</label>
            <input
              id="contact-phone"
              name="phone_number"
              type="tel"
              placeholder="Enter phone number"
              value={formData.phone_number}
              onChange={handleInputChange}
              maxLength={20}
              required
            />

            <label htmlFor="contact-relationship">Relationship</label>
            <input
              id="contact-relationship"
              name="relationship"
              type="text"
              placeholder="e.g. Parent, Friend, Sibling"
              value={formData.relationship}
              onChange={handleInputChange}
              maxLength={50}
              required
            />

            <button
              type="submit"
              className="contact-submit-button"
              disabled={saving}
            >
              {saving
                ? 'Saving...'
                : editingId
                  ? 'Update Contact'
                  : 'Add Contact'}
            </button>

            {editingId && (
              <button
                type="button"
                className="contact-cancel-button"
                onClick={resetForm}
                disabled={saving}
              >
                Cancel Editing
              </button>
            )}
          </form>
        </div>
      </div>
    </section>
  )
}