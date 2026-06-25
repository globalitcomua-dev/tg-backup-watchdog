from app.core.config import settings
from app.telegram.client import TelegramClient
from app.telegram.service import TelegramService


def run_listener() -> None:
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured")

    client = TelegramClient(settings.telegram_bot_token)
    service = TelegramService(client=client)

    service.run_forever()