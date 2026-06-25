from datetime import datetime

from pydantic import BaseModel

from app.domain.status import BackupStatus


class BackupCheckItem(BaseModel):
    host: str
    job: str
    engine: str

    expected_every_hours: int
    deadline: str | None = None

    status: BackupStatus | str

    last_run_at: datetime | None = None
    age_hours: float | None = None
    last_backup_status: str | None = None
    error_count: int | None = None
    message: str | None = None


class BackupCheckResult(BaseModel):
    counters: dict[str, int]
    items: list[BackupCheckItem]