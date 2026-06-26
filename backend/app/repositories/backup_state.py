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
    ) -> BackupState:

        state = self.get(host, job)

        if state:
            state.status = status
            state.message = message
            return state

        state = BackupState(
            host=host,
            job=job,
            status=status,
            message=message,
        )

        self.db.add(state)

        return state