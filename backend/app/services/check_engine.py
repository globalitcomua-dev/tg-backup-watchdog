from datetime import datetime, timezone
from typing import Protocol

from app.domain.check_result import BackupCheckItem, BackupCheckResult
from app.domain.status import BackupStatus


class BackupJobLike(Protocol):
    host: str
    job: str
    engine: str
    expected_every_hours: int
    deadline: str | None
    enabled: bool


class BackupRunLike(Protocol):
    host: str
    job: str
    status: str
    finished_at: datetime | None
    created_at: datetime
    error_count: int | None
    message: str | None


class BackupCheckEngine:
    def check(
        self,
        jobs: list[BackupJobLike],
        latest_runs: dict[str, BackupRunLike | None],
        now: datetime | None = None,
    ) -> BackupCheckResult:
        current_time = now or datetime.now(timezone.utc)

        counters = {
            "ok": 0,
            "warning": 0,
            "missing": 0,
            "failed": 0,
            "unknown": 0,
            "total": 0,
        }

        items: list[BackupCheckItem] = []

        for job in jobs:
            if not job.enabled:
                continue

            counters["total"] += 1

            key = self._key(job.host, job.job)
            last_run = latest_runs.get(key)

            item = self._check_one(job, last_run, current_time)

            status_key = str(item.status)

            if status_key in counters:
                counters[status_key] += 1
            else:
                counters["unknown"] += 1

            items.append(item)

        return BackupCheckResult(
            counters=counters,
            items=items,
        )

    def _check_one(
        self,
        job: BackupJobLike,
        last_run: BackupRunLike | None,
        now: datetime,
    ) -> BackupCheckItem:
        if last_run is None:
            return BackupCheckItem(
                host=job.host,
                job=job.job,
                engine=job.engine,
                expected_every_hours=job.expected_every_hours,
                deadline=job.deadline,
                status=BackupStatus.MISSING,
                last_run_at=None,
                age_hours=None,
                last_backup_status=None,
                error_count=None,
                message=None,
            )

        last_run_at = last_run.finished_at or last_run.created_at

        if last_run_at.tzinfo is None:
            last_run_at = last_run_at.replace(tzinfo=timezone.utc)

        age_hours = round((now - last_run_at).total_seconds() / 3600, 2)

        if age_hours > job.expected_every_hours:
            status: BackupStatus | str = BackupStatus.MISSING
        elif last_run.status == BackupStatus.SUCCESS.value:
            status = "ok"
        elif last_run.status == BackupStatus.WARNING.value:
            status = BackupStatus.WARNING
        elif last_run.status == BackupStatus.FAILED.value:
            status = BackupStatus.FAILED
        else:
            status = BackupStatus.UNKNOWN

        return BackupCheckItem(
            host=job.host,
            job=job.job,
            engine=job.engine,
            expected_every_hours=job.expected_every_hours,
            deadline=job.deadline,
            status=status,
            last_run_at=last_run_at,
            age_hours=age_hours,
            last_backup_status=last_run.status,
            error_count=last_run.error_count,
            message=last_run.message,
        )

    @staticmethod
    def _key(host: str, job: str) -> str:
        return f"{host}::{job}"
