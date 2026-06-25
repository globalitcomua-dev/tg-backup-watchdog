from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.domain.status import BackupStatus


class ParsedBackupMessage(BaseModel):
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
    parser_name: str
    raw: dict[str, Any] | None = None

    def to_backup_report(self) -> "BackupReport":
        from app.domain.backup_report import BackupReport

        return BackupReport(
            host=self.host,
            job=self.job,
            engine=self.engine,
            status=self.status,
            backup_type=self.backup_type,
            started_at=self.started_at,
            finished_at=self.finished_at,
            size_bytes=self.size_bytes,
            error_count=self.error_count,
            duration_seconds=self.duration_seconds,
            snapshot_id=self.snapshot_id,
            destination=self.destination,
            message=self.message,
            raw={
                "source": "parser",
                "parser_name": self.parser_name,
                "raw": self.raw,
            },
        )