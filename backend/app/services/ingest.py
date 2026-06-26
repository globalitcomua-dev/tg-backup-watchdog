from app.domain.backup_report import BackupReport
from app.parsers.dispatcher import BackupParserDispatcher
from app.services.watchdog import WatchdogService
from app.services.interfaces import BackupIngress


class BackupIngestService(BackupIngress):
    def __init__(self, watchdog: WatchdogService):
        self.watchdog = watchdog
        self.dispatcher = BackupParserDispatcher()

    def ingest_report(self, report: BackupReport):
        return self.watchdog.ingest(report)

    def ingest_raw_message(self, text: str):
        parsed = self.dispatcher.parse(text)
        report = parsed.to_backup_report()
        return self.ingest_report(report)
