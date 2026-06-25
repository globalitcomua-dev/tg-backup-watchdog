from datetime import datetime

from pydantic import BaseModel


class BackupStateChange(BaseModel):
    host: str
    job: str
    engine: str

    old_status: str | None
    new_status: str

    changed_at: datetime
    message: str | None = None