
from app.models.otp import OTPChallenge


def register_test_user(client):
    return client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "OTP Test User",
            "email": "otp-test@example.com",
            "phone_number": "2025550102",
            "password": "TestPassword123"
        }
    )


def request_test_otp(client, capsys):
    response = client.post(
        "/api/v1/auth/login/mobile/request-otp",
        json={"phone_number": "2025550102"}
    )

    assert response.status_code == 200

    output = capsys.readouterr().out
    otp = output.split("OTP: ")[-1].strip()

    return otp


def test_mobile_otp_request(client, capsys):
    register_test_user(client)

    response = client.post(
        "/api/v1/auth/login/mobile/request-otp",
        json={"phone_number": "2025550102"}
    )

    assert response.status_code == 200
    assert "message" in response.json()

    output = capsys.readouterr().out
    assert "[DEVELOPMENT OTP]" in output


def test_mobile_otp_login(client, capsys):
    register_test_user(client)

    otp = request_test_otp(client, capsys)

    response = client.post(
        "/api/v1/auth/login/mobile/verify-otp",
        json={
            "phone_number": "2025550102",
            "otp": otp
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_invalid_mobile_otp(client, capsys):
    register_test_user(client)

    request_test_otp(client, capsys)

    response = client.post(
        "/api/v1/auth/login/mobile/verify-otp",
        json={
            "phone_number": "2025550102",
            "otp": "000000"
        }
    )

    assert response.status_code == 401


def test_mobile_otp_cannot_be_reused(client, capsys):
    register_test_user(client)

    otp = request_test_otp(client, capsys)

    first_response = client.post(
        "/api/v1/auth/login/mobile/verify-otp",
        json={
            "phone_number": "2025550102",
            "otp": otp
        }
    )

    second_response = client.post(
        "/api/v1/auth/login/mobile/verify-otp",
        json={
            "phone_number": "2025550102",
            "otp": otp
        }
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 401