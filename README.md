# rl-dda-demo-back

Backend service for RL DDA demo. Tech stack: FastAPI, SQLAlchemy (async), Alembic, MySQL. Managed with Rye.

## Quick start (dev)

1) Install Rye and sync deps

```bash
rye sync
```

2) Set environment

Create `.env` in project root (see `.env.example`).

3) Run dev server

```bash
rye run uvicorn rl_dda_demo_back.main:app --reload
```

## Configuration

Environment variables (prefixed with `APP_`):

- `APP_DB_HOST`, `APP_DB_PORT`, `APP_DB_USER`, `APP_DB_PASSWORD`, `APP_DB_NAME`
- or `APP_DATABASE_URL` (e.g., `mysql+asyncmy://user:pass@host:3306/dbname`)
- `APP_CORS_ORIGINS` is configured via `.env` as a JSON array if needed.

## Project layout

- `src/rl_dda_demo_back/main.py`: FastAPI app entry
- `src/rl_dda_demo_back/config.py`: Settings
- `src/rl_dda_demo_back/db/`: DB engine/session and metadata base
- `src/rl_dda_demo_back/api/`: Routers and schemas

