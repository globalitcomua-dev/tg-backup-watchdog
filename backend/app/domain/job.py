from datetime import datetime

from pydantic import BaseModel, Field


class BackupJobDefinition(BaseModel):
    host: str = Field(min_length=1, max_length=255)
    job: str = Field(min_length=1, max_length=255)
    engine: str = Field(default="unknown", min_length=1, max_length=100)

    expected_every_hours: int = Field(default=24, ge=1)
    deadline: str | None = None
    enabled: bool = True


class BackupJobView(BackupJobDefinition):
    id: int
    created_at: datetime