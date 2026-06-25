from app.domain.report import BackupReport
from app.domain.status import BackupStatus
from app.parsers.base import BackupMessageParser
from app.parsers.utils import strip_telegram_prefix


class UnknownParser(BackupMessageParser):
    def match(self, text: str) -> bool:
        return True

    def parse(self, text: str) -> BackupReport:
        message = strip_telegram_prefix(text)

        status = BackupStatus.UNKNOWN

        if "failed" in message.lower() or "error" in message.lower() or "помил" in message.lower():
            status = BackupStatus.WARNING

        return BackupReport(
            host="unknown",
            job="unknown",
            engine="unknown",
            status=status,
            message=text,
            raw={
                "source": "parser:unknown",
                "text": text,
            },
        )