import re
from datetime import datetime

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
        first_line = message.splitlines()[0] if message.splitlines() else message
        bracket_values = re.findall(r"\[([^\]]+)\]", first_line)

        host = bracket_values[0].strip() if bracket_values else "unknown"
        job = bracket_values[1].strip() if len(bracket_values) > 1 else host

        snapshot_id = self._find_snapshot_id(message)
        status = self._detect_status(message)
        warning_count = self._find_warning_count(message)
        duration_seconds = self._find_duration_seconds(message)
        destination = self._find_value(message, "Repo")
        finished_at = self._find_datetime(message, "Finished at")

        if status == BackupStatus.SUCCESS:
            error_count = 0
        elif warning_count is not None:
            error_count = warning_count
        else:
            error_count = None

        return ParsedBackupMessage(
            parser_name="restic",
            host=host,
            job=job,
            engine="restic",
            status=status,
            finished_at=finished_at,
            duration_seconds=duration_seconds,
            snapshot_id=snapshot_id,
            destination=destination,
            error_count=error_count,
            message=text,
            raw={
                "source": "parser:restic",
                "text": text,
            },
        )

    @staticmethod
    def _detect_status(message: str) -> BackupStatus:
        lowered = message.lower()

        if "✅" in message and "ok" in lowered:
            return BackupStatus.SUCCESS
        if "⚠️" in message or "warning" in lowered:
            return BackupStatus.WARNING
        if "❌" in message or "failed" in lowered or "error" in lowered:
            return BackupStatus.FAILED

        return BackupStatus.UNKNOWN

    @staticmethod
    def _find_snapshot_id(message: str) -> str | None:
        snapshot_match = re.search(r"Snapshot:\s*snapshot\s+([a-f0-9]+)", message, re.IGNORECASE)
        if snapshot_match:
            return snapshot_match.group(1)

        saved_match = re.search(r"snapshot\s+([a-f0-9]+)\s+saved", message, re.IGNORECASE)
        if saved_match:
            return saved_match.group(1)

        return None

    @staticmethod
    def _find_warning_count(message: str) -> int | None:
        warning_match = re.search(r"Warnings:\s*(\d+)", message, re.IGNORECASE)
        if not warning_match:
            return None

        return int(warning_match.group(1))

    @staticmethod
    def _find_duration_seconds(message: str) -> int | None:
        processed_match = re.search(r"processed .* in ((?:\d+:)?\d{1,2}:\d{2})", message, re.IGNORECASE)
        if not processed_match:
            return None

        return ResticParser._parse_clock_duration(processed_match.group(1))

    @staticmethod
    def _parse_clock_duration(value: str) -> int:
        parts = [int(part) for part in value.split(":")]
        if len(parts) == 2:
            minutes, seconds = parts
            return minutes * 60 + seconds

        hours, minutes, seconds = parts
        return hours * 3600 + minutes * 60 + seconds

    @staticmethod
    def _find_value(message: str, label: str) -> str | None:
        match = re.search(rf"{re.escape(label)}:\s*(.+)", message, re.IGNORECASE)
        if not match:
            return None

        return match.group(1).strip()

    @staticmethod
    def _find_datetime(message: str, label: str) -> datetime | None:
        value = ResticParser._find_value(message, label)
        if not value:
            return None

        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None
