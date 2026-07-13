from __future__ import annotations

from datetime import datetime
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.dependencies import get_db
from app.db.base import Base
from app.main import app
from app.telegram.filters import is_allowed_chat
from app.telegram.update import TelegramMessage


def build_client(tmp_path: Path) -> TestClient:
    db_path = tmp_path / "test.db"
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )
    testing_session_local = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    settings.admin_api_token = "test-admin-token"
    settings.telegram_bot_token = ""
    settings.telegram_chat_id = ""

    return TestClient(app)


def make_admin_headers(token: str = "test-admin-token") -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def create_producer(
    client: TestClient,
    *,
    token: str = "producer-token",
    allowed_hosts: list[str] | None = None,
    allowed_jobs: list[str] | None = None,
    producer_name: str = "server-topface",
) -> None:
    response = client.post(
        "/api/v1/producers",
        headers=make_admin_headers(),
        json={
            "producer_name": producer_name,
            "token": token,
            "allowed_hosts": allowed_hosts or ["TopFace"],
            "allowed_jobs": allowed_jobs or ["TopFace"],
            "enabled": True,
            "description": "test producer",
        },
    )
    assert response.status_code == 200, response.text


def make_producer_headers(token: str = "producer-token") -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_health_reports_split_auth_configuration():
    settings.admin_api_token = "health-admin-token"
    settings.telegram_bot_token = "telegram-token"
    settings.telegram_chat_id = "12345"

    response = TestClient(app).get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert "database" not in payload
    assert payload["admin_token_configured"] is True
    assert payload["producer_auth_mode"] == "registry"
    assert payload["telegram_chat_allowlist_configured"] is True


def test_raw_report_flow_creates_run_and_check_result(tmp_path: Path):
    client = build_client(tmp_path)
    create_producer(client)
    finished_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    create_job = client.post(
        "/api/v1/jobs",
        headers=make_admin_headers(),
        json={
            "host": "TopFace",
            "job": "TopFace",
            "engine": "cobian",
            "expected_every_hours": 24,
            "enabled": True,
        },
    )
    assert create_job.status_code == 200

    ingest = client.post(
        "/api/v1/report/raw",
        headers=make_producer_headers(),
        json={
            "text": f"[24.06.2026 14:32] backup: TopFace {finished_at} "
            "** Кількість помилок: 0. Витрачено часу: 0 год, 2 хв, 9 сек. **"
        },
    )
    assert ingest.status_code == 200
    ingest_payload = ingest.json()
    assert ingest_payload["host"] == "TopFace"
    assert ingest_payload["status"] == "success"
    assert ingest_payload["raw_json"]["parser_name"] == "cobian"

    runs = client.get("/api/v1/runs", headers=make_admin_headers())
    assert runs.status_code == 200
    runs_payload = runs.json()
    assert len(runs_payload) == 1
    assert runs_payload[0]["host"] == "TopFace"

    check = client.get("/api/v1/check", headers=make_admin_headers())
    assert check.status_code == 200
    check_payload = check.json()
    assert check_payload["counters"]["total"] == 1
    assert check_payload["counters"]["ok"] == 1
    assert check_payload["counters"]["missing"] == 0
    assert check_payload["items"][0]["status"] == "ok"

    app.dependency_overrides.clear()


def test_cobian_style_raw_report_creates_run(tmp_path: Path):
    client = build_client(tmp_path)
    create_producer(client, allowed_hosts=["BiColor"], allowed_jobs=["BiColor"])

    response = client.post(
        "/api/v1/report/raw",
        headers=make_producer_headers(),
        json={
            "text": "[26.06.2026 22:53] backup: BiColor 2026-06-26 22:52:49 ** Number of errors: 0. Time elapsed: 0 hours, 46 minutes, 47 seconds. **",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["host"] == "BiColor"
    assert payload["engine"] == "cobian"
    assert payload["status"] == "success"
    assert payload["raw_json"]["parser_name"] == "cobian"

    app.dependency_overrides.clear()


def test_check_reports_missing_when_job_has_no_runs(tmp_path: Path):
    client = build_client(tmp_path)

    create_job = client.post(
        "/api/v1/jobs",
        headers=make_admin_headers(),
        json={
            "host": "Vivere",
            "job": "Vivere",
            "engine": "cobian",
            "expected_every_hours": 24,
            "enabled": True,
        },
    )
    assert create_job.status_code == 200

    check = client.get("/api/v1/check", headers=make_admin_headers())
    assert check.status_code == 200
    check_payload = check.json()
    assert check_payload["counters"]["total"] == 1
    assert check_payload["counters"]["missing"] == 1
    assert check_payload["items"][0]["status"] == "missing"

    app.dependency_overrides.clear()


def test_states_and_untracked_runs_support_admin_flow(tmp_path: Path):
    client = build_client(tmp_path)
    create_producer(client, allowed_hosts=["Pisya"], allowed_jobs=["Pisya"])
    finished_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ingest = client.post(
        "/api/v1/report/raw",
        headers=make_producer_headers(),
        json={
            "text": f"[26.06.2026 20:03] backup: Pisya {finished_at} "
            "** Number of errors: 0. Time elapsed: 1 hours, 6 minutes, 17 seconds. **"
        },
    )
    assert ingest.status_code == 200

    untracked = client.get("/api/v1/runs/untracked", headers=make_admin_headers())
    assert untracked.status_code == 200
    untracked_payload = untracked.json()
    assert len(untracked_payload) == 1
    assert untracked_payload[0]["host"] == "Pisya"

    create_job = client.post(
        "/api/v1/jobs",
        headers=make_admin_headers(),
        json={
            "host": "Pisya",
            "job": "Pisya",
            "engine": "cobian",
            "expected_every_hours": 24,
            "deadline": "03:00",
            "enabled": True,
        },
    )
    assert create_job.status_code == 200
    job_payload = create_job.json()

    states = client.get("/api/v1/states", headers=make_admin_headers())
    assert states.status_code == 200
    states_payload = states.json()
    assert len(states_payload) == 1
    assert states_payload[0]["host"] == "Pisya"
    assert states_payload[0]["status"] == "ok"

    detail = client.get(f"/api/v1/states/{job_payload['id']}", headers=make_admin_headers())
    assert detail.status_code == 200
    detail_payload = detail.json()
    assert detail_payload["job_id"] == job_payload["id"]
    assert detail_payload["host"] == "Pisya"
    assert detail_payload["latest_run_id"] is not None

    update_job = client.put(
        f"/api/v1/jobs/{job_payload['id']}",
        headers=make_admin_headers(),
        json={
            "host": "Pisya",
            "job": "Pisya-daily",
            "engine": "cobian",
            "expected_every_hours": 12,
            "deadline": "02:30",
            "enabled": False,
        },
    )
    assert update_job.status_code == 200
    update_payload = update_job.json()
    assert update_payload["job"] == "Pisya-daily"
    assert update_payload["enabled"] is False

    admin_page = client.get("/admin")
    assert admin_page.status_code == 200
    assert "Backup Watchdog Admin" in admin_page.text
    assert "Admin API Token" in admin_page.text
    assert "Manage Producers" in admin_page.text
    assert "Suggested Next Extensions" not in admin_page.text

    delete_job = client.delete(f"/api/v1/jobs/{job_payload['id']}", headers=make_admin_headers())
    assert delete_job.status_code == 200

    states_after_delete = client.get("/api/v1/states", headers=make_admin_headers())
    assert states_after_delete.status_code == 200
    assert states_after_delete.json() == []

    delete_run = client.delete(
        f"/api/v1/runs/{untracked_payload[0]['id']}",
        headers=make_admin_headers(),
    )
    assert delete_run.status_code == 200

    untracked_after_delete = client.get("/api/v1/runs/untracked", headers=make_admin_headers())
    assert untracked_after_delete.status_code == 200
    assert untracked_after_delete.json() == []

    app.dependency_overrides.clear()


def test_admin_endpoints_reject_producer_token(tmp_path: Path):
    client = build_client(tmp_path)
    create_producer(client)

    response = client.get("/api/v1/jobs", headers=make_producer_headers())

    assert response.status_code == 401

    app.dependency_overrides.clear()


def test_raw_report_rejects_admin_token(tmp_path: Path):
    client = build_client(tmp_path)

    response = client.post(
        "/api/v1/report/raw",
        headers=make_admin_headers(),
        json={"text": "[26.06.2026 22:53] backup: TopFace 2026-06-26 22:52:49 ** Number of errors: 0. Time elapsed: 0 hours, 46 minutes, 47 seconds. **"},
    )

    assert response.status_code == 401

    app.dependency_overrides.clear()


def test_raw_report_rejects_missing_token(tmp_path: Path):
    client = build_client(tmp_path)

    response = client.post(
        "/api/v1/report/raw",
        json={"text": "[26.06.2026 22:53] backup: TopFace 2026-06-26 22:52:49 ** Number of errors: 0. Time elapsed: 0 hours, 46 minutes, 47 seconds. **"},
    )

    assert response.status_code == 401

    app.dependency_overrides.clear()


def test_raw_report_rejects_foreign_host_for_producer(tmp_path: Path):
    client = build_client(tmp_path)
    create_producer(client, allowed_hosts=["TopFace"], allowed_jobs=["TopFace"])

    response = client.post(
        "/api/v1/report/raw",
        headers=make_producer_headers(),
        json={
            "text": "[26.06.2026 22:53] backup: BiColor 2026-06-26 22:52:49 ** Number of errors: 0. Time elapsed: 0 hours, 46 minutes, 47 seconds. **",
        },
    )

    assert response.status_code == 403
    assert "not allowed" in response.json()["detail"]

    app.dependency_overrides.clear()


def test_producer_registry_endpoints_require_admin_token(tmp_path: Path):
    client = build_client(tmp_path)

    response = client.get("/api/v1/producers", headers=make_producer_headers("producer-token"))

    assert response.status_code == 401

    app.dependency_overrides.clear()


def test_telegram_chat_filter_is_fail_closed():
    settings.telegram_chat_id = ""

    allowed = is_allowed_chat(
        TelegramMessage(
            update_id=1,
            message_id=1,
            chat_id="123",
            text="backup",
        )
    )

    assert allowed is False
