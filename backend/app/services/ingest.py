import logging

from app.domain.backup_report import BackupReport
from app.domain.producer import ProducerIdentity
from app.parsers.dispatcher import BackupParserDispatcher
from app.services.watchdog import WatchdogService
from app.services.interfaces import BackupIngress


logger = logging.getLogger(__name__)


class BackupIngestService(BackupIngress):
    def __init__(self, watchdog: WatchdogService):
        self.watchdog = watchdog
        self.dispatcher = BackupParserDispatcher()

    def ingest_report(self, report: BackupReport):
        return self.watchdog.ingest(report)

    def ingest_raw_message(self, text: str, producer: ProducerIdentity):
        parsed = self.dispatcher.parse(text)
        report = parsed.to_backup_report()
        self._authorize_report(report, producer)
        return self.ingest_report(report)

    def ingest_telegram_message(self, text: str):
        parsed = self.dispatcher.parse(text)
        report = parsed.to_backup_report()
        logger.info(
            "Telegram report authorized by chat allowlist",
            extra={
                "actor_type": "telegram",
                "host": report.host,
                "job": report.job,
            },
        )
        return self.ingest_report(report)

    def _authorize_report(self, report: BackupReport, producer: ProducerIdentity) -> None:
        host_allowed = not producer.allowed_hosts or report.host in producer.allowed_hosts
        job_allowed = not producer.allowed_jobs or report.job in producer.allowed_jobs

        if host_allowed and job_allowed:
            logger.info(
                "Producer authorized for report",
                extra={
                    "actor_type": "producer",
                    "producer_name": producer.producer_name,
                    "host": report.host,
                    "job": report.job,
                },
            )
            return

        logger.warning(
            "Producer authorization rejected for report",
            extra={
                "actor_type": "producer",
                "producer_name": producer.producer_name,
                "host": report.host,
                "job": report.job,
                "allowed_hosts": sorted(producer.allowed_hosts),
                "allowed_jobs": sorted(producer.allowed_jobs),
                "reason": "host/job binding mismatch",
            },
        )
        raise PermissionError(
            f"Producer {producer.producer_name} is not allowed to send reports for "
            f"{report.host}/{report.job}"
        )
