from datetime import datetime

from pydantic import BaseModel


class BackupStateView(BaseModel):
    host: str
    job: str
    engine: str
    expected_every_hours: int
    deadline: str | None = None
    enabled: bool
    status: str
    last_run_at: datetime | None = None
    age_hours: float | None = None
    last_backup_status: str | None = None
    error_count: int | None = None
    message: str | None = None
    last_changed_at: datetime | None = None
    last_notified_at: datetime | None = None


class UntrackedBackupRunView(BaseModel):
    host: str
    job: str
    engine: str
    status: str
    finished_at: datetime | None = None
    created_at: datetime
    error_count: int | None = None
    message: str | None = None
