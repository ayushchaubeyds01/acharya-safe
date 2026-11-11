
import sys
from getpass import getpass
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

# Add the backend directory to Python's import path.
BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User


def main():
    print("\nACHARYA SAFE - Admin Account Setup\n")

    full_name = input("Admin full name: ").strip()
    email = input("Admin email: ").strip()
    phone_number = input("Admin phone number: ").strip()

    password = getpass("Admin password: ")
    confirm_password = getpass("Confirm password: ")

    if len(full_name) < 2 or len(full_name) > 120:
        print("Error: Name must contain 2-120 characters.")
        return

    if "@" not in email:
        print("Error: Enter a valid email address.")
        return

    if not 10 <= len(phone_number) <= 20:
        print("Error: Phone number must contain 10-20 characters.")
        return

    if len(password) < 8 or len(password) > 128:
        print("Error: Password must contain 8-128 characters.")
        return

    if password != confirm_password:
        print("Error: Passwords do not match.")
        return

    db = SessionLocal()

    try:
        existing_user = db.scalar(
            select(User).where(
                (User.email == email)
                | (User.phone_number == phone_number)
            )
        )

        if existing_user:
            print("Error: Email or phone number is already registered.")
            return

        admin = User(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            hashed_password=hash_password(password),
            role="admin"
        )

        db.add(admin)
        db.commit()

        print("\nAdmin account created successfully.")
        print("Admin email:", admin.email)
        print("Admin role:", admin.role)

    except IntegrityError:
        db.rollback()
        print("Error: Account details already exist.")

    except Exception:
        db.rollback()
        print("Error: Admin account creation failed.")

    finally:
        db.close()


if __name__ == "__main__":
    main()