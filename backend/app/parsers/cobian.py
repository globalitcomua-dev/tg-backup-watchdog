import re
from datetime import datetime

from app.parsers.parsed_message import ParsedBackupMessage
from app.domain.status import BackupStatus
from app.parsers.base import BackupMessageParser
from app.parsers.utils import (
    parse_english_duration,
    parse_ukrainian_duration,
    strip_telegram_prefix,
)


class CobianParser(BackupMessageParser):
    def match(self, text: str) -> bool:
        message = strip_telegram_prefix(text)

        return (
            "Number of errors:" in message
            or "Кількість помилок:" in message
        )

    def parse(self, text: str) -> ParsedBackupMessage:
        message = strip_telegram_prefix(text)

        english_match = re.search(
            r"^([A-Za-z0-9_\-]+)\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}).*?"
            r"Number of errors:\s*(\d+)",
            message,
            re.IGNORECASE | re.DOTALL,
        )

        if english_match:
            host, finished_at, errors_raw = english_match.groups()
            errors = int(errors_raw)

            return ParsedBackupMessage(
                parser_name="cobian",
                host=host,
                job=host,
                engine="cobian",
                status=BackupStatus.SUCCESS if errors == 0 else BackupStatus.WARNING,
                finished_at=datetime.strptime(finished_at, "%Y-%m-%d %H:%M:%S"),
                error_count=errors,
                duration_seconds=parse_english_duration(message),
                message=text,
                raw={
                    "source": "parser:cobian",
                    "format": "english",
                    "text": text,
                },
            )

        ukrainian_match = re.search(
            r"^([A-Za-z0-9_\-]+)\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}).*?"
            r"Кількість помилок:\s*(\d+)",
            message,
            re.IGNORECASE | re.DOTALL,
        )

        if ukrainian_match:
            host, finished_at, errors_raw = ukrainian_match.groups()
            errors = int(errors_raw)

            return ParsedBackupMessage(
                parser_name="cobian",
                host=host,
                job=host,
                engine="cobian",
                status=BackupStatus.SUCCESS if errors == 0 else BackupStatus.WARNING,
                finished_at=datetime.strptime(finished_at, "%Y-%m-%d %H:%M:%S"),
                error_count=errors,
                duration_seconds=parse_ukrainian_duration(message),
                message=text,
                raw={
                    "source": "parser:cobian",
                    "format": "ukrainian",
                    "text": text,
                },
            )

        raise ValueError("Message matched CobianParser but could not be parsed")