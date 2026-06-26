from sqlalchemy.orm import Session

from app.domain.job import BackupJobDefinition
from app.domain.backup_report import BackupReport
from app.repositories.backup_job import BackupJobRepository
from app.repositories.backup_run import BackupRunRepository
from app.services.check_engine import BackupCheckEngine


class WatchdogService:
    def __init__(self, db: Session):
        self.db = db
        self.runs = BackupRunRepository(db)
        self.jobs = BackupJobRepository(db)

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
