
def create_authenticated_user(client, email="test@example.com", phone="2025550100"):
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


def test_create_emergency_contact(client):
    headers = create_authenticated_user(client)

    response = client.post(
        "/api/v1/emergency-contacts",
        headers=headers,
        json={
            "name": "John Doe",
            "phone_number": "9876543210",
            "relationship": "Brother"
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "John Doe"
    assert response.json()["phone_number"] == "9876543210"
    assert response.json()["relationship"] == "Brother"
    assert "id" in response.json()


def test_list_emergency_contacts(client):
    headers = create_authenticated_user(client)

    client.post(
        "/api/v1/emergency-contacts",
        headers=headers,
        json={
            "name": "John Doe",
            "phone_number": "9876543210",
            "relationship": "Brother"
        }
    )

    response = client.get(
        "/api/v1/emergency-contacts",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "John Doe"


def test_update_emergency_contact(client):
    headers = create_authenticated_user(client)

    create_response = client.post(
        "/api/v1/emergency-contacts",
        headers=headers,
        json={
            "name": "John Doe",
            "phone_number": "9876543210",
            "relationship": "Brother"
        }
    )

    contact_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/emergency-contacts/{contact_id}",
        headers=headers,
        json={
            "name": "Updated Name"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"
    assert response.json()["phone_number"] == "9876543210"


def test_delete_emergency_contact(client):
    headers = create_authenticated_user(client)

    create_response = client.post(
        "/api/v1/emergency-contacts",
        headers=headers,
        json={
            "name": "John Doe",
            "phone_number": "9876543210",
            "relationship": "Brother"
        }
    )

    contact_id = create_response.json()["id"]

    response = client.delete(
        f"/api/v1/emergency-contacts/{contact_id}",
        headers=headers
    )

    assert response.status_code == 204

    list_response = client.get(
        "/api/v1/emergency-contacts",
        headers=headers
    )

    assert list_response.status_code == 200
    assert list_response.json() == []


def test_unauthenticated_contact_access(client):
    response = client.get("/api/v1/emergency-contacts")

    assert response.status_code == 401


def test_user_cannot_access_another_users_contact(client):
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

    create_response = client.post(
        "/api/v1/emergency-contacts",
        headers=first_user_headers,
        json={
            "name": "Private Contact",
            "phone_number": "9876543210",
            "relationship": "Friend"
        }
    )

    contact_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/emergency-contacts/{contact_id}",
        headers=second_user_headers
    )

    assert response.status_code == 404