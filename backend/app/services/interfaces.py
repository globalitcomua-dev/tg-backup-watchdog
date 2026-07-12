from abc import ABC, abstractmethod

from app.domain.backup_report import BackupReport
from app.domain.producer import ProducerIdentity


class BackupIngress(ABC):
    @abstractmethod
    def ingest_report(self, report: BackupReport):
        raise NotImplementedError

    @abstractmethod
    def ingest_raw_message(self, text: str, producer: ProducerIdentity):
        raise NotImplementedError
