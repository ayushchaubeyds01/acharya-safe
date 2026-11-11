
# ACHARYA SAFE - Backend

FastAPI backend for the ACHARYA SAFE personal safety and emergency response platform.

## Technology Stack

- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic Settings
- JWT Authentication
- Argon2 Password Hashing
- Pytest

## Project Structure

```text
backend/
├── app/
│   ├── api/
│   │   ├── dependencies.py
│   │   └── v1/
│   │       ├── endpoints/
│   │       └── router.py
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── modules/
├── migrations/
├── scripts/
├── tests/
├── main.py
├── requirements.txt
└── .env
```

## Prerequisites

- Python 3.13
- PostgreSQL 18
- Git

## Environment Configuration

Create a `.env` file inside the backend directory.

Required environment variables:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/acharya_safe
JWT_SECRET_KEY=YOUR_SECRET_KEY
```

Replace the placeholders with your local values.

Never commit `.env` to Git.

## Installation

From the project root:

```powershell
.\backend\venv\Scripts\python.exe -m pip install -r backend/requirements.txt
```

If the virtual environment does not exist, create it first:

```powershell
python -m venv backend/venv
```

## Database Migrations

Apply all available migrations:

```powershell
.\backend\venv\Scripts\python.exe -m alembic upgrade head
```

Check the current database revision:

```powershell
.\backend\venv\Scripts\python.exe -m alembic current
```

View migration heads:

```powershell
.\backend\venv\Scripts\python.exe -m alembic heads
```

## Run the Backend

From the project root:

```powershell
.\backend\venv\Scripts\python.exe -m uvicorn main:app --reload --app-dir backend
```

Backend base URL:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/api/v1/health

## Authentication Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/auth/register` | Register a user |
| POST | `/api/v1/auth/login/email` | Email and password login |
| POST | `/api/v1/auth/login/mobile/request-otp` | Request mobile OTP |
| POST | `/api/v1/auth/login/mobile/verify-otp` | Verify OTP and log in |
| GET | `/api/v1/auth/me` | Get authenticated user profile |

Protected endpoints require a Bearer access token.

## Admin Account Setup

Create an administrator account using the local script:

```powershell
.\backend\venv\Scripts\python.exe backend/scripts/create_admin.py
```

There is no public administrator registration endpoint.

## Development OTP Service

The current SMS service is a development-only mock.

- No real SMS is sent.
- Generated OTPs are printed in the backend terminal.
- A real SMS provider will be integrated later.

## Run Automated Tests

Run the complete test suite:

```powershell
.\backend\venv\Scripts\python.exe -m pytest backend/tests -v
```

The tests use an isolated in-memory SQLite database. They do not modify the development PostgreSQL database.

## Frontend Development Origins

The backend currently allows these development origins through CORS:

- User frontend: `http://localhost:5173`
- Admin frontend: `http://localhost:5174`

Both frontends use the same backend API.

## Current Foundation

Implemented:

- Modular monolith backend structure
- PostgreSQL database connection
- SQLAlchemy models
- Alembic database migrations
- User registration
- Argon2 password hashing
- Email and password authentication
- JWT access tokens
- Mobile OTP authentication
- Role-based authorization
- Administrator account creation
- CORS configuration
- Automated tests

## Development Scope

This backend is currently a development foundation, not a production deployment.

Real SMS delivery, production security hardening, deployment configuration, and application-specific safety features will be implemented in later phases.
