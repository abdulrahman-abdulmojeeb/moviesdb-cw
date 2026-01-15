# Movies Database Coursework

A full-stack movie information application built on the GroupLens MovieLens dataset. Browse 9,700+ movies, explore genre and rating analytics, get predictive ratings, and discover personality-based viewing insights.

**Course**: COMP0022 -- UCL | **Team**: Anya, Shione, Ksenia, Abdulrahman

---

## Quick Start

```bash
git clone https://github.com/abdulrahman-abdulmojeeb/moviesdb-cw.git && cd moviesdb-cw
chmod +x setup.sh
./setup.sh
```

The setup script downloads datasets, builds containers, runs migrations, and seeds the database. Once complete:

| Service  | URL                        |
|----------|----------------------------|
| Frontend | http://localhost:5173       |
| API      | http://localhost:8000       |
| API Docs | http://localhost:8000/docs  |

> Pass `--skip-enrich` to skip optional TMDB/OMDB enrichment if you don't have API keys.

---

## Repository Structure

```
.gitignore
.env.example
docker-compose.yml
setup.sh
README.md
api/                  # FastAPI backend
  app/
    routers/          # Endpoint handlers
    queries/          # Raw SQL query modules
    utils/            # Auth helpers
  db/
    migrations/       # Schema, indexes, views
    seed/             # Data loading scripts
  tests/
frontend/             # React SPA
  src/
    components/       # Reusable UI components
    pages/            # Route pages
    context/          # Auth context
    api/              # Axios client
```

---

## Architecture

```
+-------------------+       +-------------------+
|   Frontend (x1)   | <---> |   API (x1)        |
|   React + Vite    |       |   FastAPI + uvicorn|
|   port 5173       |       |   port 8000        |
+-------------------+       +--------+----------+
                                     |
                             +-------v-------+
                             | PostgreSQL 18 |
                             | port 5432     |
                             +---------------+
```

Docker Compose runs 3 containers (db, api, frontend) on a `moviesnet` bridge network.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12+, FastAPI, psycopg2 (raw SQL) |
| Database | PostgreSQL 18 (pg_trgm, CTEs, window functions, CORR) |
| Frontend | React 19, Vite 6, Tailwind CSS v4, React Router v7 |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Containers | Docker Compose v2, multi-stage Dockerfiles |
| Data | MovieLens, Personality ISF 2018, TMDB API, OMDB API |

---

## Team

| Member | Role |
|--------|------|
| Anya | Backend lead -- API endpoints, auth, business logic |
| Shione | Frontend lead -- React pages, components, UI/UX |
| Ksenia | Data and database lead -- schema, migrations, SQL optimisation |
| Abdulrahman | Full-stack and infrastructure -- detail pages, Docker, enrichment scripts |
