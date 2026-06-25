# TG Backup Watchdog

Service for collecting, parsing and monitoring backup reports.

## Features

- REST API
- Telegram listener
- PostgreSQL storage
- Alembic migrations
- Cobian parser
- Restic parser
- Custom `[OK]` parser
- Backup health check engine
- Backup state tracking
- Docker deployment

## Quick Start

Clone repository:

```bash
git clone https://github.com/globalitcomua-dev/tg-backup-watchdog.git
cd tg-backup-watchdog
```

Create environment file:

```bash
cp .env.example .env
nano .env
```

Required values:

```env
POSTGRES_PASSWORD=change_me
DATABASE_URL=postgresql+psycopg://backup_watchdog:change_me@db:5432/backup_watchdog
API_TOKEN=change_me
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

Start API and database:

```bash
docker compose -f docker/docker-compose.prod.yml up -d --build
```

Run migrations:

```bash
docker compose -f docker/docker-compose.prod.yml exec api alembic upgrade head
```

Check API:

```bash
curl http://127.0.0.1:8088/health
```

Expected:

```json
{"status":"ok"}
```

## Telegram Listener

Start listener:

```bash
docker compose -f docker/docker-compose.prod.yml --profile telegram-listener up -d
```

View logs:

```bash
docker compose -f docker/docker-compose.prod.yml logs -f telegram-listener
```

## API examples

Send raw Telegram-style report:

```bash
TOKEN="change_me"

curl -X POST http://127.0.0.1:8088/api/v1/report/raw \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"[24.06.2026 2:39] backup: TopFace 2026-06-24 02:39:26 ** Number of errors: 2. Time elapsed: 1 hours, 49 minutes, 24 seconds. **"}'
```

List runs:

```bash
curl http://127.0.0.1:8088/api/v1/runs \
  -H "Authorization: Bearer $TOKEN"
```

Run check:

```bash
curl http://127.0.0.1:8088/api/v1/check \
  -H "Authorization: Bearer $TOKEN"
```

## Local development

Create venv:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -e .
```

Run API:

```powershell
uvicorn app.main:app --app-dir backend --reload
```

Run tests:

```powershell
python -m pytest backend\tests
```

## Project structure

```text
backend/
  app/
    api/
    core/
    db/
    domain/
    parsers/
    repositories/
    schemas/
    services/
    telegram/
  alembic/
  tests/

docker/
```

## Status

Early development.