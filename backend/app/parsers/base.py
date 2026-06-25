from abc import ABC, abstractmethod

from app.parsers.parsed_message import ParsedBackupMessage


class BackupMessageParser(ABC):
    @abstractmethod
    def match(self, text: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def parse(self, text: str) -> ParsedBackupMessage:
        raise NotImplementedError