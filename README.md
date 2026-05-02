# Blog FastAPI (GraphQL)

Minimal FastAPI + GraphQL blog example (project root: e:\FastApi\Blog_Fast_API)

Features
- FastAPI app with Ariadne GraphQL endpoint (/graphql) and WebSocket GraphQL.
- SQLAlchemy models + DB engine (alembic migrations recommended).
- Redis cache (fastapi-cache2).
- Celery for background workers (notes mention celery_worker.celery_app).
- Rate limiter, admin UI (sqladmin), session middleware.
- Example startup uses Redis at redis://localhost.

Prerequisites
- Docker & Docker Compose (recommended)
- Python 3.11+ (for local dev)
- Redis, Postgres (or your DB) for prod/dev
- Optional: Celery & Flower for background tasks

Environment variables
- SECRET_KEY (session middleware)
- DATABASE_URL (e.g. postgresql+psycopg2://user:pass@db:5432/blog)
- REDIS_URL (e.g. redis://redis:6379/0)
- CELERY_BROKER_URL (usually same as REDIS_URL)
- CELERY_RESULT_BACKEND (usually same as REDIS_URL)
- Any other settings used in blog/*.py (check blog/database, blog/settings)

Local dev (without Docker)
1. Create virtualenv and install deps:
   pip install -r requirements.txt
2. Set env vars (SECRET_KEY, DATABASE_URL, REDIS_URL, ...)
3. Create DB tables (or run alembic migrations)
   - If using SQLAlchemy create_all: app's main currently calls models.Base.metadata.create_all(engine)
   - Alembic example (if configured):
     alembic -c blog/alembic.ini revision --autogenerate -m "init"
     alembic -c blog/alembic.ini upgrade head
4. Run:
   uvicorn blog.main:app --reload --host 0.0.0.0 --port 8000
   GraphQL endpoint: http://localhost:8000/graphql

Celery (local)
- Worker: celery -A celery_worker.celery_app worker --pool=solo --loglevel=info
- Flower: celery -A celery_worker.celery_app flower --port=5555

Docker (recommended)
- Build and run all services with Docker Compose (see docker-compose.yml).
- Edit .env or compose env section for secrets.

Notes
- Check blog/database.py for engine/session configuration and required DB driver (psycopg2/binary or asyncpg).
- Check celery_worker.* to confirm celery application path and any extra services.
- Adjust Dockerfile/compose if project layout or entrypoint differs.

Contact
- This README is generated from project files in e:\FastApi\Blog_Fast_API. Adjust env values and paths to match your setup.