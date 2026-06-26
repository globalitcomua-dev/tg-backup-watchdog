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


def build_client(tmp_path: Path) -> TestClient:
    db_path = tmp_path / "test.db"
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )
    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    settings.api_token = "test-token"

    client = TestClient(app)
    client.headers.update({"Authorization": "Bearer test-token"})
    return client


def test_health_does_not_leak_database_url():
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert "database" not in payload
    assert "database_configured" in payload


def test_raw_report_flow_creates_run_and_check_result(tmp_path: Path):
    client = build_client(tmp_path)
    finished_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    create_job = client.post(
        "/api/v1/jobs",
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

    runs = client.get("/api/v1/runs")
    assert runs.status_code == 200
    runs_payload = runs.json()
    assert len(runs_payload) == 1
    assert runs_payload[0]["host"] == "TopFace"

    check = client.get("/api/v1/check")
    assert check.status_code == 200
    check_payload = check.json()
    assert check_payload["counters"]["total"] == 1
    assert check_payload["counters"]["ok"] == 1
    assert check_payload["counters"]["missing"] == 0
    assert check_payload["items"][0]["status"] == "ok"

    app.dependency_overrides.clear()


def test_check_reports_missing_when_job_has_no_runs(tmp_path: Path):
    client = build_client(tmp_path)

    create_job = client.post(
        "/api/v1/jobs",
        json={
            "host": "Vivere",
            "job": "Vivere",
            "engine": "cobian",
            "expected_every_hours": 24,
            "enabled": True,
        },
    )
    assert create_job.status_code == 200

    check = client.get("/api/v1/check")
    assert check.status_code == 200
    check_payload = check.json()
    assert check_payload["counters"]["total"] == 1
    assert check_payload["counters"]["missing"] == 1
    assert check_payload["items"][0]["status"] == "missing"

    app.dependency_overrides.clear()


def test_states_and_untracked_runs_support_admin_flow(tmp_path: Path):
    client = build_client(tmp_path)
    finished_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ingest = client.post(
        "/api/v1/report/raw",
        json={
            "text": f"[26.06.2026 20:03] backup: Pisya {finished_at} "
            "** Number of errors: 0. Time elapsed: 1 hours, 6 minutes, 17 seconds. **"
        },
    )
    assert ingest.status_code == 200

    untracked = client.get("/api/v1/runs/untracked")
    assert untracked.status_code == 200
    untracked_payload = untracked.json()
    assert len(untracked_payload) == 1
    assert untracked_payload[0]["host"] == "Pisya"

    create_job = client.post(
        "/api/v1/jobs",
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

    states = client.get("/api/v1/states")
    assert states.status_code == 200
    states_payload = states.json()
    assert len(states_payload) == 1
    assert states_payload[0]["host"] == "Pisya"
    assert states_payload[0]["status"] == "ok"

    update_job = client.put(
        f"/api/v1/jobs/{job_payload['id']}",
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

    app.dependency_overrides.clear()
