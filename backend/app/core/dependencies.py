from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.watchdog import WatchdogService
from app.services.ingest import BackupIngestService


def get_watchdog_service(db: Session = Depends(get_db)) -> WatchdogService:
    return WatchdogService(db)

def get_ingest_service(
    watchdog=Depends(get_watchdog_service),
):
    return BackupIngestService(watchdog)