from abc import ABC, abstractmethod

from app.domain.backup_report import BackupReport


class BackupIngress(ABC):
    @abstractmethod
    def ingest_report(self, report: BackupReport):
        raise NotImplementedError

    @abstractmethod
    def ingest_raw_message(self, text: str):
        raise NotImplementedError