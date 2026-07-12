from app.services.ingest import BackupIngestService
from app.telegram.update import TelegramMessage


class BackupMessageHandler:
    def __init__(self, ingest: BackupIngestService):
        self.ingest = ingest

    def handle(self, message: TelegramMessage):
        return self.ingest.ingest_telegram_message(message.text)
