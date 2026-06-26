from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import BackupState


class BackupStateRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, host: str, job: str) -> BackupState | None:
        return self.db.scalars(
            select(BackupState)
            .where(BackupState.host == host)
            .where(BackupState.job == job)
        ).first()

    def list_all(self) -> list[BackupState]:
        return list(
            self.db.scalars(select(BackupState))
        )

    def save(
        self,
        host: str,
        job: str,
        status: str,
        message: str | None,
        changed_at: datetime | None = None,
    ) -> BackupState:
        current_time = changed_at or datetime.now(timezone.utc)

        state = self.get(host, job)

        if state:
            if state.status != status:
                state.last_changed_at = current_time
            state.status = status
            state.message = message
            return state

        state = BackupState(
            host=host,
            job=job,
            status=status,
            message=message,
            last_changed_at=current_time,
        )

        self.db.add(state)

        return state

    def mark_notified(
        self,
        host: str,
        job: str,
        notified_at: datetime | None = None,
    ) -> BackupState | None:
        state = self.get(host, job)

        if not state:
            return None

        state.last_notified_at = notified_at or datetime.now(timezone.utc)
        return state
