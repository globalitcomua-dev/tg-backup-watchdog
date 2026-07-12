from app.core.config import settings
from app.telegram.update import TelegramMessage


def is_allowed_chat(message: TelegramMessage) -> bool:
    if not settings.telegram_chat_id:
        return False

    return message.chat_id == str(settings.telegram_chat_id)


def is_command(message: TelegramMessage) -> bool:
    return message.text.strip().startswith("/")


def is_backup_message(message: TelegramMessage) -> bool:
    text = message.text

    markers = [
        "Number of errors:",
        "Кількість помилок:",
        "Restic backup",
        "[OK]",
        "backup",
    ]

    return any(marker in text for marker in markers)
