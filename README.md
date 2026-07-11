# Odoo Hackathon

Full-stack application with a FastAPI backend and frontend.

## Project Structure

```
├── backend/          # FastAPI application
├── frontend/         # Frontend application
├── docker-compose.yml
└── README.md
```

## Getting Started

### Backend (local)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env     # if .env does not exist
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://localhost:8000/docs

### Docker

```bash
docker compose up --build
```

## Environment Variables

Copy `backend/.env.example` to `backend/.env` and update values as needed.
