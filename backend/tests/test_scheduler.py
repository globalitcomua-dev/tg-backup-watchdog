from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.backup_report import BackupReport
from app.domain.job import BackupJobDefinition
from app.domain.status import BackupStatus
from app.db.base import Base
from app.repositories.backup_state import BackupStateRepository
from app.scheduler.service import BackupMonitorScheduler
from app.services.state_service import BackupStateService
from app.services.watchdog import WatchdogService


class RecordingNotifier:
    def __init__(self):
        self.changes = []

    def send_state_changes(self, changes):
        self.changes.extend(changes)
        return len(changes)


def create_session_factory(tmp_path: Path):
    engine = create_engine(
        f"sqlite:///{tmp_path / 'scheduler.db'}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


def test_state_service_marks_last_changed_only_on_real_change(tmp_path: Path):
    SessionLocal = create_session_factory(tmp_path)

    with SessionLocal() as db:
        repository = BackupStateRepository(db)
        first = repository.save("TopFace", "Nightly", "ok", "All good")
        db.commit()
        original_changed_at = first.last_changed_at

        second = repository.save("TopFace", "Nightly", "ok", "Still good")
        db.commit()
        assert second.last_changed_at == original_changed_at

        third = repository.save("TopFace", "Nightly", "warning", "Now warning")
        db.commit()
        assert third.last_changed_at >= original_changed_at


def test_scheduler_sends_notification_on_status_change(tmp_path: Path, monkeypatch):
    SessionLocal = create_session_factory(tmp_path)
    notifier = RecordingNotifier()

    with SessionLocal() as db:
        watchdog = WatchdogService(db)
        watchdog.create_or_update_job(
            BackupJobDefinition(
                host="TopFace",
                job="TopFace",
                engine="custom",
                expected_every_hours=24,
                enabled=True,
            )
        )

        watchdog.ingest(
            BackupReport(
                host="TopFace",
                job="TopFace",
                engine="custom",
                status=BackupStatus.SUCCESS,
                message="[OK] TopFace",
                raw={"source": "test"},
            )
        )

    monkeypatch.setattr("app.scheduler.service.SessionLocal", SessionLocal)

    scheduler = BackupMonitorScheduler(
        notification_service=notifier,
        notify_on_initial=False,
        check_interval=1,
    )

    first = scheduler.run_once()
    assert first.changes_detected == 0
    assert first.notifications_sent == 0

    with SessionLocal() as db:
        watchdog = WatchdogService(db)
        watchdog.ingest(
            BackupReport(
                host="TopFace",
                job="TopFace",
                engine="custom",
                status=BackupStatus.FAILED,
                message="Backup failed badly",
                raw={"source": "test"},
            )
        )

    second = scheduler.run_once()
    assert second.changes_detected == 1
    assert second.notifications_sent == 1
    assert notifier.changes[0].old_status == "ok"
    assert notifier.changes[0].new_status == "failed"

    with SessionLocal() as db:
        state_service = BackupStateService(BackupStateRepository(db))
        persisted = state_service.repository.get("TopFace", "TopFace")
        assert persisted is not None
        assert persisted.last_notified_at is not None
