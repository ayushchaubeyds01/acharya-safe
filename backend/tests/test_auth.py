
def register_test_user(client):
    """Register a test user and return the response."""

    return client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test User",
            "email": "test@example.com",
            "phone_number": "2025550100",
            "password": "TestPassword123"
        }
    )


def test_user_registration(client):
    response = register_test_user(client)

    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    assert response.json()["role"] == "user"


def test_duplicate_registration(client):
    first_response = register_test_user(client)
    second_response = register_test_user(client)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_email_login(client):
    register_test_user(client)

    response = client.post(
        "/api/v1/auth/login/email",
        json={
            "email": "test@example.com",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_invalid_email_login(client):
    response = client.post(
        "/api/v1/auth/login/email",
        json={
            "email": "test@example.com",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401


def test_authenticated_user_profile(client):
    register_test_user(client)

    login_response = client.post(
        "/api/v1/auth/login/email",
        json={
            "email": "test@example.com",
            "password": "TestPassword123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert response.json()["role"] == "user"


def test_unauthenticated_profile_access(client):
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401
