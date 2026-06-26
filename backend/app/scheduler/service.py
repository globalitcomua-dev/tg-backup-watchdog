import time
from dataclasses import dataclass

from app.core.config import settings
from app.db.session import SessionLocal
from app.repositories.backup_state import BackupStateRepository
from app.services.state_service import BackupStateService
from app.services.watchdog import WatchdogService
from app.telegram.client import TelegramClient
from app.telegram.notifications import TelegramNotificationService


@dataclass
class SchedulerRunResult:
    total_jobs: int
    changes_detected: int
    notifications_sent: int


class BackupMonitorScheduler:
    def __init__(
        self,
        notification_service: TelegramNotificationService | None = None,
        check_interval: int | None = None,
        notify_on_initial: bool | None = None,
    ):
        self.notification_service = notification_service
        self.check_interval = (
            check_interval if check_interval is not None else settings.watchdog_check_interval
        )
        self.notify_on_initial = (
            notify_on_initial if notify_on_initial is not None else settings.notify_on_initial_state
        )

    @classmethod
    def from_settings(cls) -> "BackupMonitorScheduler":
        notification_service = None

        if settings.telegram_bot_token and settings.telegram_chat_id:
            notification_service = TelegramNotificationService(
                client=TelegramClient(settings.telegram_bot_token),
            )

        return cls(notification_service=notification_service)

    def run_once(self) -> SchedulerRunResult:
        with SessionLocal() as db:
            watchdog = WatchdogService(db)
            state_service = BackupStateService(BackupStateRepository(db))

            check_result = watchdog.check_result()
            changes = state_service.detect(
                check_result,
                notify_on_initial=self.notify_on_initial,
            )

            notifications_sent = 0
            if changes and self.notification_service is not None:
                notifications_sent = self.notification_service.send_state_changes(changes)
                state_service.mark_changes_notified(changes)

            db.commit()

            return SchedulerRunResult(
                total_jobs=check_result.counters["total"],
                changes_detected=len(changes),
                notifications_sent=notifications_sent,
            )

    def run_forever(self) -> None:
        print("Backup monitor scheduler started", flush=True)

        while True:
            try:
                result = self.run_once()
                print(
                    "Scheduler cycle completed "
                    f"jobs={result.total_jobs} "
                    f"changes={result.changes_detected} "
                    f"notifications={result.notifications_sent}",
                    flush=True,
                )
            except Exception as exc:
                print(f"Scheduler error: {exc}", flush=True)

            time.sleep(self.check_interval)
