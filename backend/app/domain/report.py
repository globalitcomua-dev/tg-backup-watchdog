from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.domain.status import BackupStatus


class BackupReport(BaseModel):
    host: str
    job: str
    engine: str
    status: BackupStatus

    backup_type: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    size_bytes: int | None = None
    error_count: int | None = None
    duration_seconds: int | None = None
    snapshot_id: str | None = None
    destination: str | None = None

    message: str | None = None
    raw: dict[str, Any] | None = None