def send_otp_sms(phone_number: str, otp: str) -> bool:
    """
    Development-only mock SMS delivery.
    Does not send a real SMS.
    """

    print(
        f"[DEVELOPMENT OTP] Phone: {phone_number} | OTP: {otp}"
    )

    return True   