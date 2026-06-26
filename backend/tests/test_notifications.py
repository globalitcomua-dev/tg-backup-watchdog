from datetime import datetime, timezone

from app.domain.state import BackupStateChange
from app.telegram.notifications import TelegramNotificationService


class DummyTelegramClient:
    def __init__(self):
        self.sent_messages: list[dict] = []

    def send_message(self, chat_id: str, text: str) -> dict:
        self.sent_messages.append(
            {
                "chat_id": chat_id,
                "text": text,
            }
        )
        return {"message_id": len(self.sent_messages)}


def test_format_state_change_contains_context():
    change = BackupStateChange(
        host="TopFace",
        job="Nightly",
        engine="restic",
        old_status="ok",
        new_status="warning",
        changed_at=datetime(2026, 6, 26, 10, 0, tzinfo=timezone.utc),
        message="2 errors found",
    )

    text = TelegramNotificationService.format_state_change(change)

    assert "Backup WARNING" in text
    assert "Host: TopFace" in text
    assert "Job: Nightly" in text
    assert "State: ok -> warning" in text
    assert "2 errors found" in text


def test_send_state_changes_sends_one_message_per_change():
    client = DummyTelegramClient()
    service = TelegramNotificationService(client=client, chat_id="12345")

    changes = [
        BackupStateChange(
            host="TopFace",
            job="Nightly",
            engine="restic",
            old_status="ok",
            new_status="failed",
            changed_at=datetime(2026, 6, 26, 10, 0, tzinfo=timezone.utc),
            message="Backup failed",
        )
    ]

    sent_count = service.send_state_changes(changes)

    assert sent_count == 1
    assert client.sent_messages[0]["chat_id"] == "12345"
    assert "Backup FAILED" in client.sent_messages[0]["text"]
