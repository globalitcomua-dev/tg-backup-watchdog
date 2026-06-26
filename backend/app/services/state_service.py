from datetime import datetime, timezone

from app.domain.check_result import BackupCheckResult
from app.domain.state import BackupStateChange
from app.repositories.backup_state import BackupStateRepository
from app.services.state_engine import BackupStateEngine


class BackupStateService:

    def __init__(self, repository: BackupStateRepository):
        self.repository = repository
        self.engine = BackupStateEngine()

    def detect(
        self,
        check_result: BackupCheckResult,
        notify_on_initial: bool = False,
        now: datetime | None = None,
    ) -> list[BackupStateChange]:
        current_time = now or datetime.now(timezone.utc)
        previous = {
            f"{s.host}::{s.job}": s.status
            for s in self.repository.list_all()
        }

        changes = self.engine.detect_changes(
            check_result,
            previous,
            notify_on_initial=notify_on_initial,
            now=current_time,
        )

        for item in check_result.items:
            self.repository.save(
                host=item.host,
                job=item.job,
                status=str(item.status),
                message=item.message,
                changed_at=current_time,
            )

        return changes

    def mark_changes_notified(
        self,
        changes: list[BackupStateChange],
        notified_at: datetime | None = None,
    ) -> None:
        current_time = notified_at or datetime.now(timezone.utc)

        for change in changes:
            self.repository.mark_notified(
                host=change.host,
                job=change.job,
                notified_at=current_time,
            )
