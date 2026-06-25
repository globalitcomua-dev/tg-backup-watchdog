from datetime import datetime, timezone

from app.domain.check_result import BackupCheckResult
from app.domain.state import BackupStateChange


class BackupStateEngine:
    @staticmethod
    def key(host: str, job: str) -> str:
        return f"{host}::{job}"

    def detect_changes(
        self,
        check_result: BackupCheckResult,
        previous_states: dict[str, str],
        notify_on_initial: bool = False,
        now: datetime | None = None,
    ) -> list[BackupStateChange]:
        current_time = now or datetime.now(timezone.utc)
        changes: list[BackupStateChange] = []

        for item in check_result.items:
            key = self.key(item.host, item.job)
            old_status = previous_states.get(key)
            new_status = str(item.status)

            if old_status is None and not notify_on_initial:
                continue

            if old_status == new_status:
                continue

            changes.append(
                BackupStateChange(
                    host=item.host,
                    job=item.job,
                    engine=item.engine,
                    old_status=old_status,
                    new_status=new_status,
                    changed_at=current_time,
                    message=item.message,
                )
            )

        return changes