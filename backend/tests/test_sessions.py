
from sqlalchemy import select

from app.core.config import settings
from app.core.token import hash_refresh_token
from app.models.refresh_session import RefreshSession


def register_test_user(client):
    return client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Session Test User",
            "email": "session@example.com",
            "phone_number": "2025550199",
            "password": "TestPassword123"
        }
    )


def login_test_user(client):
    register_test_user(client)

    return client.post(
        "/api/v1/auth/login/email",
        json={
            "email": "session@example.com",
            "password": "TestPassword123"
        }
    )


def test_login_creates_hashed_refresh_session(client, db_session):
    response = login_test_user(client)

    assert response.status_code == 200
    assert "access_token" in response.json()

    refresh_token = client.cookies.get(
        settings.REFRESH_COOKIE_NAME
    )

    assert refresh_token is not None

    cookie_header = response.headers["set-cookie"].lower()

    assert "httponly" in cookie_header
    assert "samesite=lax" in cookie_header

    session = db_session.scalar(
        select(RefreshSession).where(
            RefreshSession.token_hash == hash_refresh_token(
                refresh_token
            )
        )
    )

    assert session is not None
    assert session.used_at is None
    assert session.revoked_at is None
    assert session.token_hash != refresh_token


def test_refresh_token_rotation(client, db_session):
    login_response = login_test_user(client)

    assert login_response.status_code == 200

    old_refresh_token = client.cookies.get(
        settings.REFRESH_COOKIE_NAME
    )

    response = client.post(
        "/api/v1/auth/refresh",
        headers={"Origin": "http://localhost:5173"}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()

    new_refresh_token = client.cookies.get(
        settings.REFRESH_COOKIE_NAME
    )

    assert new_refresh_token is not None
    assert new_refresh_token != old_refresh_token

    old_session = db_session.scalar(
        select(RefreshSession).where(
            RefreshSession.token_hash == hash_refresh_token(
                old_refresh_token
            )
        )
    )

    new_session = db_session.scalar(
        select(RefreshSession).where(
            RefreshSession.token_hash == hash_refresh_token(
                new_refresh_token
            )
        )
    )

    assert old_session.used_at is not None
    assert new_session is not None
    assert old_session.session_id == new_session.session_id


def test_reused_refresh_token_revokes_session(
    client,
    db_session
):
    login_response = login_test_user(client)

    assert login_response.status_code == 200

    original_token = client.cookies.get(
        settings.REFRESH_COOKIE_NAME
    )

    first_refresh = client.post(
        "/api/v1/auth/refresh",
        headers={"Origin": "http://localhost:5173"}
    )

    assert first_refresh.status_code == 200

    rotated_token = client.cookies.get(
        settings.REFRESH_COOKIE_NAME
    )

    # Simulate reuse of the previously consumed token.
    client.cookies.set(
        settings.REFRESH_COOKIE_NAME,
        original_token,
        path=settings.REFRESH_COOKIE_PATH
    )

    replay_response = client.post(
        "/api/v1/auth/refresh",
        headers={"Origin": "http://localhost:5173"}
    )

    assert replay_response.status_code == 401

    session_records = db_session.scalars(
        select(RefreshSession).where(
            RefreshSession.token_hash.in_([
                hash_refresh_token(original_token),
                hash_refresh_token(rotated_token)
            ])
        )
    ).all()

    assert len(session_records) == 2
    assert all(
        record.revoked_at is not None
        for record in session_records
    )


def test_logout_revokes_refresh_session(client, db_session):
    login_response = login_test_user(client)

    assert login_response.status_code == 200

    refresh_token = client.cookies.get(
        settings.REFRESH_COOKIE_NAME
    )

    response = client.post(
        "/api/v1/auth/logout",
        headers={"Origin": "http://localhost:5173"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"

    session = db_session.scalar(
        select(RefreshSession).where(
            RefreshSession.token_hash == hash_refresh_token(
                refresh_token
            )
        )
    )

    assert session.revoked_at is not None