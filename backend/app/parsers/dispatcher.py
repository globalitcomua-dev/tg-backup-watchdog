from app.parsers.base import BackupMessageParser
from app.parsers.cobian import CobianParser
from app.parsers.custom import CustomOkParser
from app.parsers.parsed_message import ParsedBackupMessage
from app.parsers.restic import ResticParser
from app.parsers.unknown import UnknownParser


class BackupParserDispatcher:
    def __init__(self, parsers: list[BackupMessageParser] | None = None):
        self.parsers = parsers or [
            CobianParser(),
            ResticParser(),
            CustomOkParser(),
            UnknownParser(),
        ]

    def parse(self, text: str) -> ParsedBackupMessage:
        for parser in self.parsers:
            if parser.match(text):
                return parser.parse(text)

        raise ValueError("No parser matched the message")