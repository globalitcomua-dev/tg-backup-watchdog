from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.backup_report import BackupReport
from app.db.models import BackupRun


class BackupRunRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, report: BackupReport) -> BackupRun:
        run = BackupRun(
            host=report.host,
            job=report.job,
            engine=report.engine,
            status=report.status.value,
            backup_type=report.backup_type,
            started_at=report.started_at,
            finished_at=report.finished_at,
            size_bytes=report.size_bytes,
            error_count=report.error_count,
            duration_seconds=report.duration_seconds,
            snapshot_id=report.snapshot_id,
            destination=report.destination,
            message=report.message,
            raw_json=report.raw,
        )

        self.db.add(run)
        self.db.flush()

        return run

    def get(self, run_id: int) -> BackupRun | None:
        return self.db.get(BackupRun, run_id)

    def latest(self, limit: int = 100) -> list[BackupRun]:
        stmt = (
            select(BackupRun)
            .order_by(BackupRun.id.desc())
            .limit(limit)
        )

        return list(self.db.scalars(stmt))

    def latest_by_job(self, host: str, job: str) -> BackupRun | None:
        stmt = (
            select(BackupRun)
            .where(
                BackupRun.host == host,
                BackupRun.job == job,
            )
            .order_by(BackupRun.id.desc())
            .limit(1)
        )

        return self.db.scalars(stmt).first()

    def latest_for_jobs(self, jobs: list) -> dict[str, BackupRun | None]:
        result: dict[str, BackupRun | None] = {}

        for job in jobs:
            key = f"{job.host}::{job.job}"
            result[key] = self.latest_by_job(job.host, job.job)

        return result

    def latest_unique(self, limit: int = 100) -> list[BackupRun]:
        unique_runs: list[BackupRun] = []
        seen: set[str] = set()

        for run in self.latest(limit=limit):
            key = f"{run.host}::{run.job}"
            if key in seen:
                continue
            seen.add(key)
            unique_runs.append(run)

        return unique_runs
