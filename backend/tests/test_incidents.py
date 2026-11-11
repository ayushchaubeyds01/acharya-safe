
from uuid import UUID

from app.modules.incidents.schemas.incident import IncidentCreate
from app.modules.incidents.services.incident_service import create_incident


def create_authenticated_user(
    client,
    email="test@example.com",
    phone="2025550100"
):
    """Register and authenticate a test user."""

    registration_response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test User",
            "email": email,
            "phone_number": phone,
            "password": "TestPassword123"
        }
    )

    assert registration_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login/email",
        json={
            "email": email,
            "password": "TestPassword123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def create_internal_incident(
    client,
    db_session,
    headers,
    activation_source="voice",
    severity="unknown"
):
    """Create an incident through the internal service."""

    user_response = client.get(
        "/api/v1/auth/me",
        headers=headers
    )

    assert user_response.status_code == 200

    user_id = UUID(user_response.json()["id"])

    return create_incident(
        db_session,
        user_id,
        IncidentCreate(
            activation_source=activation_source,
            severity=severity,
            description="Test emergency incident",
            location={
                "latitude": 26.8467,
                "longitude": 80.9462,
                "accuracy": 10
            }
        )
    )


def test_list_incidents_empty(client):
    headers = create_authenticated_user(client)

    response = client.get(
        "/api/v1/incidents",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json() == []


def test_list_incidents(client, db_session):
    headers = create_authenticated_user(client)

    create_internal_incident(
        client,
        db_session,
        headers,
        activation_source="voice",
        severity="high"
    )

    response = client.get(
        "/api/v1/incidents",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["activation_source"] == "voice"
    assert response.json()[0]["severity"] == "high"
    assert response.json()[0]["status"] == "detected"


def test_retrieve_incident(client, db_session):
    headers = create_authenticated_user(client)

    incident = create_internal_incident(
        client,
        db_session,
        headers
    )

    response = client.get(
        f"/api/v1/incidents/{incident.id}",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["id"] == str(incident.id)
    assert response.json()["description"] == "Test emergency incident"


def test_unauthenticated_incident_access(client):
    response = client.get("/api/v1/incidents")

    assert response.status_code == 401


def test_user_cannot_access_another_users_incident(
    client,
    db_session
):
    first_user_headers = create_authenticated_user(
        client,
        email="first@example.com",
        phone="2025550101"
    )

    second_user_headers = create_authenticated_user(
        client,
        email="second@example.com",
        phone="2025550102"
    )

    incident = create_internal_incident(
        client,
        db_session,
        first_user_headers
    )

    response = client.get(
        f"/api/v1/incidents/{incident.id}",
        headers=second_user_headers
    )

    assert response.status_code == 404


def test_users_cannot_create_incidents_through_public_api(client):
    headers = create_authenticated_user(client)

    response = client.post(
        "/api/v1/incidents",
        headers=headers,
        json={
            "activation_source": "manual"
        }
    )

    assert response.status_code == 405