from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import TelegramOffset


class TelegramOffsetRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_last_update_id(self, bot_name: str) -> int | None:
        offset = self.db.scalars(
            select(TelegramOffset).where(TelegramOffset.bot_name == bot_name)
        ).first()

        if not offset:
            return None

        return offset.last_update_id

    def save_last_update_id(self, bot_name: str, update_id: int) -> TelegramOffset:
        offset = self.db.scalars(
            select(TelegramOffset).where(TelegramOffset.bot_name == bot_name)
        ).first()

        if offset:
            offset.last_update_id = update_id
        else:
            offset = TelegramOffset(
                bot_name=bot_name,
                last_update_id=update_id,
            )
            self.db.add(offset)

        self.db.flush()
        return offset