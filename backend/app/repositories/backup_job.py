from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.job import BackupJobDefinition
from app.db.models import BackupJob


class BackupJobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, definition: BackupJobDefinition) -> BackupJob:
        job = BackupJob(
            host=definition.host,
            job=definition.job,
            engine=definition.engine,
            expected_every_hours=definition.expected_every_hours,
            deadline=definition.deadline,
            enabled=definition.enabled,
        )

        self.db.add(job)
        self.db.flush()

        return job

    def list(self) -> list[BackupJob]:
        stmt = (
            select(BackupJob)
            .order_by(
                BackupJob.host,
                BackupJob.job,
            )
        )

        return list(self.db.scalars(stmt))

    def get(self, host: str, job: str) -> BackupJob | None:
        stmt = (
            select(BackupJob)
            .where(
                BackupJob.host == host,
                BackupJob.job == job,
            )
        )

        return self.db.scalars(stmt).first()