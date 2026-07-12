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
ADMIN_API_TOKEN=change_me_admin
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

Expected minimal shape:

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

## Scheduler

Start periodic monitoring:

```bash
docker compose -f docker/docker-compose.prod.yml --profile watchdog-scheduler up -d
```

View logs:

```bash
docker compose -f docker/docker-compose.prod.yml logs -f watchdog-scheduler
```

## API examples

Send raw Telegram-style report:

```bash
PRODUCER_TOKEN="change_me_producer"

curl -X POST http://127.0.0.1:8088/api/v1/report/raw \
  -H "Authorization: Bearer $PRODUCER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"[24.06.2026 2:39] backup: TopFace 2026-06-24 02:39:26 ** Number of errors: 2. Time elapsed: 1 hours, 49 minutes, 24 seconds. **"}'
```

Send Cobian-style report through the shared raw ingest:

```bash
PRODUCER_TOKEN="change_me_producer"

curl -X POST http://127.0.0.1:8088/api/v1/report/raw \
  -H "Authorization: Bearer $PRODUCER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text":"[26.06.2026 22:53] backup: BiColor 2026-06-26 22:52:49 ** Number of errors: 0. Time elapsed: 0 hours, 46 minutes, 47 seconds. **"
  }'
```

List runs with the admin token:

```bash
ADMIN_TOKEN="change_me_admin"

curl http://127.0.0.1:8088/api/v1/runs \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

Run check:

```bash
curl http://127.0.0.1:8088/api/v1/check \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

## Local development

Create venv:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -e .[dev]
```

Run API:

```powershell
uvicorn app.main:app --app-dir backend --reload
```

Run tests:

```powershell
python -m pytest backend\tests
```

## Cobian sender

For a transition away from Telegram-based ingestion, use [examples/cobian_send_report.ps1](/E:/Devel/tg-backup-watchdog/examples/cobian_send_report.ps1:1). It sends a single text payload into the shared `report/raw` ingest, so parsing still goes through the normal Cobian parser.

Example:

```powershell
.\\examples\\cobian_send_report.ps1 `
  -ApiUrl "http://127.0.0.1:8088" `
  -ProducerToken "change_me_producer" `
  -Host "TopFace" `
  -FinishedAt "2026-06-26 16:34:22" `
  -ErrorCount 0 `
  -DurationSeconds 600
```

If you need a ready-to-adapt script instead of a minimal contract example, use [examples/cobian_send_full.ps1](/E:/Devel/tg-backup-watchdog/examples/cobian_send_full.ps1:1). It adds defaults, validation, English/Ukrainian message generation, error handling, and optional `WATCHDOG_PRODUCER_TOKEN` environment-variable support.

Example:

```powershell
$env:WATCHDOG_PRODUCER_TOKEN = "change_me_producer"

.\\examples\\cobian_send_full.ps1 `
  -ApiUrl "http://127.0.0.1:8088" `
  -Host "BiColor" `
  -FinishedAt "2026-06-26 22:52:49" `
  -ErrorCount 0 `
  -DurationSeconds 2807 `
  -Language en
```

## Restic watchdog template

Use [examples/restic_watchdog_template.ps1](/E:/Devel/tg-backup-watchdog/examples/restic_watchdog_template.ps1:1) as the canonical summary format for restic reports sent into the shared `report/raw` ingest.

Recommended minimal message shape:

```text
[WIN-272627A7S64] [Amstar] ⚠️ WARNING Restic backup
Finished at: 2026-06-26 21:28:04
Exit code: 3
Files:           2 new,     7 changed, 291432 unmodified
Dirs:            0 new,     9 changed, 27534 unmodified
Added to the repository: 1.288 GiB (1.234 GiB stored)
processed 291441 files, 103.916 GiB in 5:18
Snapshot: snapshot 37231659
Warnings: 1
Message: at least one source file could not be read
```

Keep this payload short and monitoring-focused. Do not include repo paths, log file paths, prune output, or long diagnostic tails in the watchdog text.

## Auth model

- `ADMIN_API_TOKEN` is only for:
  - `/admin`
  - job management
  - producer management
  - summary/check/state/runs admin endpoints
- producer tokens are only for:
  - `/api/v1/report/raw`

Producer tokens are stored in the producer registry, not in `.env`, and each producer can be restricted to specific `host` and `job` values.

## Producer registry operations

Create a producer with the admin token:

```bash
ADMIN_TOKEN="change_me_admin"

curl -X POST http://127.0.0.1:8088/api/v1/producers \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "producer_name":"server-topface",
    "token":"change_me_producer",
    "allowed_hosts":["TopFace"],
    "allowed_jobs":["TopFace"],
    "enabled":true,
    "description":"TopFace backup sender"
  }'
```

List producers:

```bash
curl http://127.0.0.1:8088/api/v1/producers \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

Rotate or update a producer:

```bash
curl -X PUT http://127.0.0.1:8088/api/v1/producers/1 \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "producer_name":"server-topface",
    "token":"change_me_producer_v2",
    "allowed_hosts":["TopFace"],
    "allowed_jobs":["TopFace"],
    "enabled":true,
    "description":"Rotated token"
  }'
```

Disable a compromised producer by updating it with `"enabled": false` or delete it entirely.

## Telegram listener security

Telegram ingest is now fail-closed:

- if `TELEGRAM_BOT_TOKEN` is configured but `TELEGRAM_CHAT_ID` is empty, the listener must not run
- messages from chats outside the allowlist are skipped

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
