from app.core.config import settings
from app.domain.state import BackupStateChange
from app.telegram.client import TelegramClient


STATUS_TITLES = {
    "ok": "Backup OK",
    "warning": "Backup WARNING",
    "failed": "Backup FAILED",
    "missing": "Backup MISSING",
    "unknown": "Backup UNKNOWN",
}

STATUS_EMOJI = {
    "ok": "🟢",
    "warning": "🟡",
    "failed": "🔴",
    "missing": "🔴",
    "unknown": "⚪",
}


class TelegramNotificationService:
    def __init__(self, client: TelegramClient, chat_id: str | None = None):
        self.client = client
        self.chat_id = chat_id or settings.telegram_chat_id

    def send_state_changes(self, changes: list[BackupStateChange]) -> int:
        if not self.chat_id:
            raise RuntimeError("TELEGRAM_CHAT_ID is not configured")

        sent_count = 0

        for change in changes:
            self.client.send_message(
                chat_id=self.chat_id,
                text=self.format_state_change(change),
            )
            sent_count += 1

        return sent_count

    @staticmethod
    def format_state_change(change: BackupStateChange) -> str:
        new_status = change.new_status
        emoji = STATUS_EMOJI.get(new_status, "⚪")
        title = STATUS_TITLES.get(new_status, f"Backup {new_status.upper()}")

        lines = [
            f"{emoji} {title}",
            f"Host: {change.host}",
            f"Job: {change.job}",
            f"Engine: {change.engine}",
        ]

        if change.old_status is not None:
            lines.append(f"State: {change.old_status} -> {change.new_status}")
        else:
            lines.append(f"State: {change.new_status}")

        if change.message:
            lines.append("")
            lines.append("Message:")
            lines.append(change.message)

        return "\n".join(lines)
