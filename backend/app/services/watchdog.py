from sqlalchemy.orm import Session

from app.domain.job import BackupJobDefinition
from app.domain.backup_report import BackupReport
from app.repositories.backup_state import BackupStateRepository
from app.repositories.backup_job import BackupJobRepository
from app.repositories.backup_run import BackupRunRepository
from app.schemas.state import BackupStateView, UntrackedBackupRunView
from app.services.check_engine import BackupCheckEngine


class WatchdogService:
    def __init__(self, db: Session):
        self.db = db
        self.runs = BackupRunRepository(db)
        self.jobs = BackupJobRepository(db)
        self.states = BackupStateRepository(db)

    def ingest(self, report: BackupReport):
        run = self.runs.create(report)
        self.db.commit()
        self.db.refresh(run)
        return run

    def create_or_update_job(self, definition: BackupJobDefinition):
        existing = self.jobs.get(definition.host, definition.job)

        if existing:
            existing.engine = definition.engine
            existing.expected_every_hours = definition.expected_every_hours
            existing.deadline = definition.deadline
            existing.enabled = definition.enabled

            self.db.commit()
            self.db.refresh(existing)
            return existing

        job = self.jobs.create(definition)
        self.db.commit()
        self.db.refresh(job)
        return job

    def update_job(self, job_id: int, definition: BackupJobDefinition):
        existing = self.jobs.get_by_id(job_id)

        if existing is None:
            return None

        existing.host = definition.host
        existing.job = definition.job
        existing.engine = definition.engine
        existing.expected_every_hours = definition.expected_every_hours
        existing.deadline = definition.deadline
        existing.enabled = definition.enabled

        self.db.commit()
        self.db.refresh(existing)
        return existing

    def list_jobs(self):
        return self.jobs.list()

    def history(self, limit: int = 100):
        limit = min(limit, 500)
        return self.runs.latest(limit)

    def summary(self):
        latest = {}

        for run in self.runs.latest(limit=1000):
            key = f"{run.host}::{run.job}"

            if key in latest:
                continue

            latest[key] = {
                "host": run.host,
                "job": run.job,
                "engine": run.engine,
                "status": run.status,
                "error_count": run.error_count,
                "duration_seconds": run.duration_seconds,
                "snapshot_id": run.snapshot_id,
                "last_run_at": run.finished_at or run.created_at,
                "created_at": run.created_at,
                "message": run.message,
            }

        items = list(latest.values())

        counters = {
            "success": 0,
            "warning": 0,
            "failed": 0,
            "unknown": 0,
            "total": len(items),
        }

        for item in items:
            status = item["status"]

            if status in counters:
                counters[status] += 1
            else:
                counters["unknown"] += 1

        return {
            "counters": counters,
            "items": items,
        }

    def check(self):
        return self.check_result().model_dump()

    def check_result(self):
        jobs = self.jobs.list()
        latest_runs = self.runs.latest_for_jobs(jobs)

        engine = BackupCheckEngine()

        return engine.check(
            jobs=jobs,
            latest_runs=latest_runs,
        )

    def list_states(self) -> list[BackupStateView]:
        check_result = self.check_result()
        persisted_states = {
            f"{state.host}::{state.job}": state
            for state in self.states.list_all()
        }
        jobs = {
            f"{job.host}::{job.job}": job
            for job in self.jobs.list()
        }

        items: list[BackupStateView] = []
        for item in check_result.items:
            key = f"{item.host}::{item.job}"
            persisted = persisted_states.get(key)
            job = jobs[key]
            items.append(
                BackupStateView(
                    host=item.host,
                    job=item.job,
                    engine=item.engine,
                    expected_every_hours=item.expected_every_hours,
                    deadline=item.deadline,
                    enabled=job.enabled,
                    status=str(item.status),
                    last_run_at=item.last_run_at,
                    age_hours=item.age_hours,
                    last_backup_status=item.last_backup_status,
                    error_count=item.error_count,
                    message=item.message,
                    last_changed_at=persisted.last_changed_at if persisted else None,
                    last_notified_at=persisted.last_notified_at if persisted else None,
                )
            )

        return items

    def list_untracked_runs(self, limit: int = 100) -> list[UntrackedBackupRunView]:
        tracked_keys = {
            f"{job.host}::{job.job}"
            for job in self.jobs.list()
        }
        items: list[UntrackedBackupRunView] = []

        for run in self.runs.latest_unique(limit=limit):
            key = f"{run.host}::{run.job}"
            if key in tracked_keys:
                continue

            items.append(
                UntrackedBackupRunView(
                    host=run.host,
                    job=run.job,
                    engine=run.engine,
                    status=run.status,
                    finished_at=run.finished_at,
                    created_at=run.created_at,
                    error_count=run.error_count,
                    message=run.message,
                )
            )

        return items
