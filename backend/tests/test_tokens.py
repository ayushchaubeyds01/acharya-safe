
from datetime import datetime, timedelta, timezone

import jwt
import pytest

from app.core.config import settings
from app.core.token import create_access_token, decode_access_token


def test_valid_access_token():
    token = create_access_token("test-user-id")

    payload = decode_access_token(token)

    assert payload["sub"] == "test-user-id"
    assert payload["type"] == "access"


def test_invalid_token_signature():
    token = jwt.encode(
        {
            "sub": "test-user-id",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
            "type": "access"
        },
        "incorrect-secret-key-that-is-at-least-32-bytes",
        algorithm=settings.JWT_ALGORITHM
    )

    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(token)


def test_wrong_token_type():
    token = jwt.encode(
        {
            "sub": "test-user-id",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
            "type": "refresh"
        },
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(token)


def test_expired_access_token():
    token = jwt.encode(
        {
            "sub": "test-user-id",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=5),
            "type": "access"
        },
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(token)


def test_missing_token_subject():
    token = jwt.encode(
        {
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
            "type": "access"
        },
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(token)
