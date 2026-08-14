# AegisRisk GRC Platform

AegisRisk is an enterprise-grade Governance, Risk, and Compliance (GRC) platform that centralizes cybersecurity risk management. It combines a FastAPI backend (Python) with a React + TypeScript frontend, a PostgreSQL database, Redis for caching/queues, Celery for async jobs, and Nginx for production reverse-proxying.

Key goals: asset inventory, STRIDE threat modeling, automated risk scoring, framework control catalogs (NIST / ISO / SOC2), and an interactive dashboard for risk analytics.

---

## Table of Contents

- [What this is](#what-this-is)
- [Key features](#key-features)
- [Stack](#stack)
- [Project structure](#project-structure-top-level)
- [Quick start (development)](#quick-start--development-local)
- [Production deployment](#production-deployment-containerized)
- [Environment variables](#environment-variables)
- [Database migrations & seeding](#database-migrations--seeding)
- [Health checks & verification](#health-checks--verification)
- [Running tests](#running-tests)
- [Development tips](#development-tips)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Project report & documentation](#project-report--documentation)
- [License & acknowledgements](#license--acknowledgements)

---

## What this is

A full-stack, containerized GRC platform with:

- **Backend:** FastAPI + SQLAlchemy + Alembic
- **Frontend:** React + TypeScript + Vite + Tailwind
- **Supporting services:** PostgreSQL, Redis, Celery, Nginx

Designed for demo, evaluation, and iterative development; production-ready with containerized deployments and an Nginx reverse proxy.

### Key features

- JWT-based authentication and user / organization management
- Asset CRUD and criticality scoring
- STRIDE threat modeling and threat-to-asset linking
- Automated risk scoring and historical risk storage
- Control framework catalogs with mapping (NIST, ISO, SOC2, PCI, HIPAA, GDPR)
- Interactive dashboard visualizations (heatmap, compliance radar, etc.)
- Asynchronous report generation (Celery) and reporting engine
- Dockerized Dev / Prod compose files and Nginx configuration

---

## Stack

- **Language(s):** Python 3.11, TypeScript (React)
- **Backend framework:** FastAPI
- **Frontend tooling:** React 18 + Vite, Tailwind CSS
- **DB & queue:** PostgreSQL, Redis, Celery
- **Other:** SQLAlchemy, Alembic, Recharts, Redux Toolkit

---

## Project structure (top-level)

```text
.env.example                     # Example env vars
docker-compose.yml               # Dev compose
docker-compose.prod.yml          # Production compose
nginx/                           # Nginx production config
frontend/                         # React + TypeScript frontend (Vite)
backend/                          # FastAPI backend, migrations, scripts
PROJECT_REPORT.md                # Project report & architecture notes
verify_setup.py                  # Lightweight health/auth verification script
```

### How it fits together

- `frontend` serves the SPA (Vite dev server in development; built assets served by Nginx in production).
- `backend` exposes REST API on port `8000` with automatic OpenAPI docs at `/docs`.
- PostgreSQL holds persisted data; Alembic manages schema migrations.
- Redis acts as Celery broker and caching layer.
- Nginx is used in production as reverse proxy and static file server.

---

## Quick start — Development (local)

### Prerequisites

- Docker & Docker Compose (v1.29+ / Compose v2 recommended)
- Git
- Node.js + npm (for local frontend development if not using containers)

### 1. Clone

```bash
git clone https://github.com/PraveenMudalgeri/AegisRisk-Platform.git
cd AegisRisk-Platform
```

### 2. Copy environment file and edit as needed

```bash
cp .env.example .env
# Edit .env to set SECRET_KEY and any credentials you need
```

### 3. Start services (development)

```bash
docker-compose up --build
```

Services:

- Backend API: `http://localhost:8000`
- Frontend (Vite dev server): `http://localhost:3000`
- API docs: `http://localhost:8000/docs`

### 4. Optional: Run frontend locally without containers

```bash
cd frontend
npm install
npm run dev
```

The frontend dev server typically runs on `http://localhost:3000`.

---

## Production deployment (containerized)

### 1. Build and start production services

From the repository root:

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

### 2. Run database migrations

```bash
docker-compose -f docker-compose.prod.yml exec backend python3 -m alembic upgrade head
```

### 3. Seed demonstration/initial data

If the seed script is provided:

```bash
docker-compose -f docker-compose.prod.yml exec backend python3 scripts/seed_production_data.py
```

### 4. Access application

Open:

```text
http://localhost
```

Nginx will serve the frontend and route API requests.

---

## Environment variables

A sample is provided in `.env.example`. Copy it to `.env`:

```bash
cp .env.example .env
```

Important variables include:

- `SECRET_KEY` — change for production
- `ALGORITHM` — e.g. `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `REFRESH_TOKEN_EXPIRE_DAYS`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_SERVER`
- `POSTGRES_PORT`
- `POSTGRES_DB`
- `REDIS_HOST`
- `REDIS_PORT`

Be sure to set a strong `SECRET_KEY` and secure database credentials for production.

---

## Database migrations & seeding

Migrations are managed with Alembic in `backend/alembic`.

### Apply migrations locally

```bash
docker-compose exec backend python3 -m alembic upgrade head
```

### Apply migrations in production

```bash
docker-compose -f docker-compose.prod.yml exec backend python3 -m alembic upgrade head
```

### Seed data

Seeding scripts live under `backend/scripts`.

For example:

```bash
docker-compose -f docker-compose.prod.yml exec backend python3 scripts/seed_production_data.py
```

Use them after migrations to populate demonstration data.

---

## Health checks & verification

A lightweight verification script is provided at the repository root:

```bash
python3 verify_setup.py
```

Or run it inside the backend container:

```bash
docker-compose exec backend python3 /path/to/verify_setup.py
```

The script performs basic health and authentication flow checks against `http://localhost:8000` by default.

---

## Running tests

If tests are included, run them inside the backend container or in a configured Python virtual environment:

```bash
docker-compose exec backend pytest
```

Adjust the command according to the test framework present in the repository.

---

## Development tips

### FastAPI

FastAPI auto-reloads in development when run with `uvicorn --reload`.

Example:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

The frontend uses Vite. Run:

```bash
npm run dev
```

inside the `frontend/` directory for hot reload.

### Docker

Use Docker volumes in the development compose configuration to pick up live code changes.

---

## Troubleshooting

### Database migrations fail

Confirm the database connection environment variables:

- `POSTGRES_SERVER`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

### Celery tasks are not processed

Verify that:

- Redis is reachable.
- The Celery worker is running.

### Check container logs

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f redis
```

---

## Contributing

Contributions are welcome.

Suggested workflow:

1. Fork and create a feature branch.
2. Add tests for new behavior where appropriate.
3. Open a pull request describing your changes.
4. Update documentation and migration scripts when making database model changes.

---

## Project report & documentation

See [`PROJECT_REPORT.md`](PROJECT_REPORT.md) for an extensive architecture overview, feature list, deployment notes, and roadmap.

---

## License & acknowledgements

No license file is included in the repository at the time of writing.

Add a `LICENSE` file (MIT, Apache-2.0, etc.) if you intend to publish the project or accept contributions under a standard license.

---

## Maintainer

**Praveen Mudalgeri** — repository owner / lead developer
