from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.domain.status import BackupStatus


class BackupReportRequest(BaseModel):
    host: str = Field(min_length=1, max_length=255)
    job: str = Field(min_length=1, max_length=255)
    engine: str = Field(min_length=1, max_length=100)
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


class BackupRunResponse(BaseModel):
    id: int
    host: str
    job: str
    engine: str
    status: str

    backup_type: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    size_bytes: int | None = None
    error_count: int | None = None
    duration_seconds: int | None = None
    snapshot_id: str | None = None
    destination: str | None = None
    message: str | None = None
    raw_json: dict[str, Any] | None = None
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }