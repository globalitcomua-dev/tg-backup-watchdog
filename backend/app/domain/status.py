from enum import Enum


class BackupStatus(str, Enum):
    SUCCESS = "success"
    WARNING = "warning"
    FAILED = "failed"
    UNKNOWN = "unknown"
    MISSING = "missing"

    def __str__(self) -> str:
        return self.value
