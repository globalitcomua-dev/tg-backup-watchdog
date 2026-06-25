import time

from app.core.config import settings
from app.db.session import SessionLocal
from app.repositories.telegram_offset import TelegramOffsetRepository
from app.services.ingest import BackupIngestService
from app.services.watchdog import WatchdogService
from app.telegram.client import TelegramClient
from app.telegram.filters import is_allowed_chat, is_backup_message, is_command
from app.telegram.handlers.backup import BackupMessageHandler
from app.telegram.handlers.unknown import UnknownMessageHandler
from app.telegram.update import parse_update


class TelegramService:
    def __init__(self, client: TelegramClient, bot_name: str = "default"):
        self.client = client
        self.bot_name = bot_name

    def poll_once(self) -> None:
        with SessionLocal() as db:
            offset_repo = TelegramOffsetRepository(db)
            last_update_id = offset_repo.get_last_update_id(self.bot_name)

        offset = last_update_id + 1 if last_update_id is not None else None
        updates = self.client.get_updates(offset=offset, timeout=30)

        for update in updates:
            self.process_update(update)

    def process_update(self, update: dict) -> None:
        update_id = update["update_id"]
        message = parse_update(update)

        with SessionLocal() as db:
            offset_repo = TelegramOffsetRepository(db)

            try:
                if not message:
                    offset_repo.save_last_update_id(self.bot_name, update_id)
                    db.commit()
                    return

                if not is_allowed_chat(message):
                    print(f"Skip chat_id={message.chat_id}", flush=True)
                    offset_repo.save_last_update_id(self.bot_name, update_id)
                    db.commit()
                    return

                watchdog = WatchdogService(db)
                ingest = BackupIngestService(watchdog)

                if is_backup_message(message):
                    handler = BackupMessageHandler(ingest)
                    run = handler.handle(message)

                    print(
                        f"Saved telegram message_id={message.message_id} "
                        f"host={run.host} job={run.job} status={run.status}",
                        flush=True,
                    )

                elif is_command(message):
                    print(f"Command ignored: {message.text}", flush=True)

                else:
                    UnknownMessageHandler().handle(message)

                offset_repo.save_last_update_id(self.bot_name, update_id)
                db.commit()

            except Exception:
                db.rollback()
                raise

    def run_forever(self) -> None:
        print("Telegram service started", flush=True)

        while True:
            try:
                self.poll_once()
            except Exception as exc:
                print(f"Telegram service error: {exc}", flush=True)
                time.sleep(settings.telegram_poll_interval)