# rl-dda-demo-back

Backend service for RL DDA demo. Tech stack: FastAPI, SQLAlchemy (async), Alembic, MySQL. Managed with Rye.

## Quick start (dev)

1) Install Rye and sync deps

```bash
rye sync
```

2) Set environment

Create `.env` in project root (see below example).

Example `.env`:

```
APP_DB_HOST=127.0.0.1
APP_DB_PORT=3306
APP_DB_USER=app
APP_DB_PASSWORD=app
APP_DB_NAME=rldda
# or: APP_DATABASE_URL=mysql+aiomysql://app:app@127.0.0.1:3306/rldda
```

3) Run dev server

```bash
rye run uvicorn rl_dda_demo_back.main:app --reload
```

## Configuration

Environment variables (prefixed with `APP_`):

- `APP_DB_HOST`, `APP_DB_PORT`, `APP_DB_USER`, `APP_DB_PASSWORD`, `APP_DB_NAME`
- or `APP_DATABASE_URL` (e.g., `mysql+aiomysql://user:pass@host:3306/dbname`)
- `APP_CORS_ORIGINS` is configured via `.env` as a JSON array if needed.

## Project layout

- `src/rl_dda_demo_back/main.py`: FastAPI app entry
- `src/rl_dda_demo_back/config.py`: Settings
- `src/rl_dda_demo_back/db/`: DB engine/session and metadata base
- `src/rl_dda_demo_back/api/`: Routers and schemas

## Database and migrations

- Start MySQL via Docker Compose (if Docker available):

```bash
docker compose up -d db
```

- Create initial migration and upgrade (requires DB running):

```bash
rye run alembic revision -m "init schema v1" --autogenerate
rye run alembic upgrade head
```

If Docker is not available on your machine, install MySQL locally and set `APP_DATABASE_URL` accordingly.


