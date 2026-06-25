import re

from app.parsers.parsed_message import ParsedBackupMessage
from app.domain.status import BackupStatus
from app.parsers.base import BackupMessageParser
from app.parsers.utils import strip_telegram_prefix


class CustomOkParser(BackupMessageParser):
    def match(self, text: str) -> bool:
        message = strip_telegram_prefix(text)

        return "[OK]" in message or "✅" in message

    def parse(self, text: str) -> ParsedBackupMessage:
        message = strip_telegram_prefix(text)

        host = "custom"

        host_match = re.search(r"\[OK\]\s+([A-Za-z0-9_\-]+)", message)

        if host_match:
            host = host_match.group(1)

        return ParsedBackupMessage(
            parser_name="custom-ok",
            host=host,
            job=host,
            engine="custom",
            status=BackupStatus.SUCCESS,
            error_count=0,
            message=text,
            raw={
                "source": "parser:custom-ok",
                "text": text,
            },
        )