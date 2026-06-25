from abc import ABC, abstractmethod

from app.domain.report import BackupReport


class BackupMessageParser(ABC):
    @abstractmethod
    def match(self, text: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def parse(self, text: str) -> BackupReport:
        raise NotImplementedError