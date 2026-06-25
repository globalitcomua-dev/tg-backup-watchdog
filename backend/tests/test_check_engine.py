from datetime import datetime, timedelta, timezone

from app.db.models import BackupJob, BackupRun
from app.domain.status import BackupStatus
from app.services.check_engine import BackupCheckEngine


def make_job(
    host: str,
    job: str,
    expected_every_hours: int = 24,
    enabled: bool = True,
) -> BackupJob:
    return BackupJob(
        host=host,
        job=job,
        engine="test",
        expected_every_hours=expected_every_hours,
        enabled=enabled,
    )


def make_run(
    host: str,
    job: str,
    status: str,
    finished_at: datetime,
    error_count: int | None = None,
) -> BackupRun:
    return BackupRun(
        host=host,
        job=job,
        engine="test",
        status=status,
        finished_at=finished_at,
        error_count=error_count,
    )


def test_check_missing_when_no_run():
    engine = BackupCheckEngine()
    job = make_job("host1", "job1")

    result = engine.check(
        jobs=[job],
        latest_runs={},
        now=datetime(2026, 6, 25, 8, 0, tzinfo=timezone.utc),
    )

    assert result.counters["missing"] == 1
    assert result.counters["total"] == 1
    assert result.items[0].status == BackupStatus.MISSING


def test_check_ok_when_success_is_fresh():
    engine = BackupCheckEngine()
    now = datetime(2026, 6, 25, 8, 0, tzinfo=timezone.utc)

    job = make_job("host1", "job1", expected_every_hours=24)
    run = make_run(
        "host1",
        "job1",
        BackupStatus.SUCCESS.value,
        finished_at=now - timedelta(hours=2),
    )

    result = engine.check(
        jobs=[job],
        latest_runs={"host1::job1": run},
        now=now,
    )

    assert result.counters["ok"] == 1
    assert result.items[0].status == "ok"
    assert result.items[0].age_hours == 2.0


def test_check_warning_when_latest_run_has_warning():
    engine = BackupCheckEngine()
    now = datetime(2026, 6, 25, 8, 0, tzinfo=timezone.utc)

    job = make_job("host1", "job1", expected_every_hours=24)
    run = make_run(
        "host1",
        "job1",
        BackupStatus.WARNING.value,
        finished_at=now - timedelta(hours=3),
        error_count=2,
    )

    result = engine.check(
        jobs=[job],
        latest_runs={"host1::job1": run},
        now=now,
    )

    assert result.counters["warning"] == 1
    assert result.items[0].status == BackupStatus.WARNING
    assert result.items[0].error_count == 2


def test_check_missing_when_success_is_too_old():
    engine = BackupCheckEngine()
    now = datetime(2026, 6, 25, 8, 0, tzinfo=timezone.utc)

    job = make_job("host1", "job1", expected_every_hours=24)
    run = make_run(
        "host1",
        "job1",
        BackupStatus.SUCCESS.value,
        finished_at=now - timedelta(hours=30),
    )

    result = engine.check(
        jobs=[job],
        latest_runs={"host1::job1": run},
        now=now,
    )

    assert result.counters["missing"] == 1
    assert result.items[0].status == BackupStatus.MISSING
    assert result.items[0].age_hours == 30.0


def test_check_ignores_disabled_jobs():
    engine = BackupCheckEngine()
    job = make_job("host1", "job1", enabled=False)

    result = engine.check(
        jobs=[job],
        latest_runs={},
        now=datetime(2026, 6, 25, 8, 0, tzinfo=timezone.utc),
    )

    assert result.counters["total"] == 0
    assert result.items == []