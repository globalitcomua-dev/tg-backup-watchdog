from app.domain.backup_report import BackupReport
from app.parsers.dispatcher import BackupParserDispatcher
from app.services.watchdog import WatchdogService
from app.services.interfaces import BackupIngress


class BackupIngestService(BackupIngress):
    def __init__(self, watchdog: WatchdogService):
        self.watchdog = watchdog
        self.dispatcher = BackupParserDispatcher()

    def ingest_raw_message(self, text: str):
        parsed = self.dispatcher.parse(text)

        report = BackupReport(
            host=parsed.host,
            job=parsed.job,
            engine=parsed.engine,
            status=parsed.status,
            backup_type=parsed.backup_type,
            started_at=parsed.started_at,
            finished_at=parsed.finished_at,
            size_bytes=parsed.size_bytes,
            error_count=parsed.error_count,
            duration_seconds=parsed.duration_seconds,
            snapshot_id=parsed.snapshot_id,
            destination=parsed.destination,
            message=parsed.message,
            raw_json={
                "parser": parsed.parser_name,
                "raw": parsed.raw,
            },
        )

        return self.watchdog.ingest(report)