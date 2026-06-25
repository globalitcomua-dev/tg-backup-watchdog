from enum import StrEnum


class BackupStatus(StrEnum):
    SUCCESS = "success"
    WARNING = "warning"
    FAILED = "failed"
    UNKNOWN = "unknown"
    MISSING = "missing"