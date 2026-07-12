# EcoSphere AI

EcoSphere AI is a full-stack ESG management MVP that helps organizations track carbon, manage CSR initiatives, monitor governance policies, and surface AI-driven recommendations from a single workspace.

## Features

- Role-based authentication for Administrator, ESG Manager, Department Manager, Employee, and Auditor
- Carbon tracking and emissions insights
- CSR activity management
- Governance policy publishing and tracking
- AI copilot-style guidance for ESG questions
- Report and analytics summaries for executive review

## Tech Stack

- Backend: FastAPI, SQLAlchemy, Pydantic, SQLite
- Frontend: React, TypeScript, Vite
- Auth: JWT-based role-aware authentication

## Project Structure

```text
backend/        # FastAPI backend and API routes
frontend/       # React + TypeScript frontend
Dockerfile      # Backend container setup
docker-compose.yml
README.md
```

## Getting Started

### 1. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The API will be available at:
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

### 2. Frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

Open the app at:
- http://localhost:5173/

### 3. Docker

```bash
docker compose up --build
```

## Authentication

Users can sign up with a selected role and sign in to access a tailored workspace. The backend returns a JWT and role-based permissions for each account.

## Testing

```bash
cd backend
python -m pytest -q tests/test_auth_roles.py
```

## Notes

- The current MVP uses SQLite for local development.
- The app is designed to be extended with PostgreSQL, production auth, and richer analytics in later iterations.