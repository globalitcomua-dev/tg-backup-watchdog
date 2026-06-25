import re

from app.parsers.parsed_message import ParsedBackupMessage
from app.domain.status import BackupStatus
from app.parsers.base import BackupMessageParser
from app.parsers.utils import strip_telegram_prefix


class ResticParser(BackupMessageParser):
    def match(self, text: str) -> bool:
        message = strip_telegram_prefix(text)

        return "Restic backup" in message

    def parse(self, text: str) -> ParsedBackupMessage:
        message = strip_telegram_prefix(text)

        host_match = re.search(r"^\[([^\]]+)\].*?Restic backup", message, re.IGNORECASE | re.DOTALL)

        if host_match:
            host = host_match.group(1).strip()
        else:
            host = "unknown"

        snapshot_id = None
        snapshot_match = re.search(r"Snapshot:\s*snapshot\s+([a-f0-9]+)", message, re.IGNORECASE)

        if snapshot_match:
            snapshot_id = snapshot_match.group(1)

        status = BackupStatus.UNKNOWN

        if "✅" in message and "OK" in message:
            status = BackupStatus.SUCCESS
        elif "⚠️" in message or "warning" in message.lower():
            status = BackupStatus.WARNING
        elif "failed" in message.lower() or "error" in message.lower():
            status = BackupStatus.FAILED

        return ParsedBackupMessage(
            parser_name="restic",
            host=host,
            job=host,
            engine="restic",
            status=status,
            snapshot_id=snapshot_id,
            error_count=0 if status == BackupStatus.SUCCESS else None,
            message=text,
            raw={
                "source": "parser:restic",
                "text": text,
            },
        )