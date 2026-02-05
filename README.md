# AegisRisk Platform - Quickstart Guide

## Prerequisites
- Docker & Docker Compose
- Git

## Production Quickstart
Run the application in a production-like environment with Nginx, optimized Javascript, and persistent databases.

### 1. Start the Stack
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```
*Wait for a minute for all containers to initialize (DB, Backend, Frontend).*

### 2. Run Database Migrations
Initialize the database schema:
```bash
docker-compose -f docker-compose.prod.yml exec backend python3 -m alembic upgrade head
```

### 3. Seed Demo Data
Populate the app with Assets, Risks, and Controls:
```bash
docker-compose -f docker-compose.prod.yml exec backend python3 scripts/seed_production_data.py
```

### 4. Access the Application
Open your browser to:
**http://localhost**

---

## Development Mode
If you want to edit code and see changes live:
```bash
docker-compose up --build
```
Access at: http://localhost:3000

## Login Credentials
- **Default User**: (You may need to register a new user at `/login` first, or check `seed_production_data.py` if it creates one)
- The seed script currently *does not* create a user. You should **Sign Up** on the login page.
